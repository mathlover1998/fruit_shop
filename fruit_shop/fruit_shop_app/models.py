from django.db import models
from django.contrib.auth.models import AbstractUser,PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator,EmailValidator
import random
from django.core.exceptions import ValidationError,ObjectDoesNotExist
from django.contrib.auth.models import Permission
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
from django.utils import timezone
# Create your models here.
GENDER = (("male", "Male"), ("female", "Female"), ("other", "Other"))

# POSITION = (
#     ("employee", "Employee"),
#     ("inventory_manager", "Inventory Manager"),
#     ("sales_associate", "Sales Associate"),
#     ("cashier", "Cashier"),
#     ("store_manager", "Store Manager"),
#     ("assistant_manager", "Assistant Manager"),
#     ("delivery_driver", "Delivery Driver"),
#     ("produce_specialist", "Produce Specialist"),
#     ("customer_service_representative", "Customer Service Representative"),
# )

UNIT = (
    ("kg", "Kilogram"),
    ("gr", "Gram"),
    ("set", "Set"),
    ("pack", "Pack"),
    ("unit", "Unit"),
)


DISCOUNT_TYPE = (("percentage", "Percentage"), ("fixed_amount", "Fixed Amount"))

APPLIES_TO_CHOICES = (
        ('all_products', 'All Products'),
        ('category', 'Category'),
        ('specific_products', 'Specific Products'),
    )

PAYMENT_METHOD = (("cash", "Cash"), ("momo", "Momo"))
class User(AbstractUser,PermissionsMixin):
    phone = models.CharField(max_length=20, null=True)
    gender = models.CharField(
        max_length=20, choices=GENDER, default="other", null=False
    )
    dob = models.DateField(default="2000-01-01")
    image = models.ImageField(
        upload_to="images/user_images/", default="images/default/default_avatar.png"
    )
    receive_updates = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    approval_email_sent = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        Group,
        blank=True,
        related_name="user_memberships"  # Specify a unique related_name
    )
    # user_permissions = models.ManyToManyField(Permission, blank=True, related_name="user_permissions")

    def save(self, *args, **kwargs):
        # Set default password if password is not provided
        if not self.pk and not self.password:
            self.set_password("012198218")  # Default password
        super().save(*args, **kwargs)

    def get_full_name(self):
        full_name = f"{self.first_name}"
        full_name += " "
        full_name += f"{self.last_name}"
        return full_name

    class Meta:
        managed = True
        db_table = "Users"
        verbose_name = "User"
        verbose_name_plural = "Users"
        indexes = [models.Index(fields=["first_name", "last_name"], name="full_name")]


class Employee(models.Model):
    hire_date = models.DateField(null=True)
    salary = models.IntegerField(null=False, default=0)
    department = models.CharField(max_length=200, default="", null=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employee")

    def __str__(self) -> str:
        return self.user.username
    class Meta:
        ordering = ["id"]
        db_table = "Employees"
        managed = True
        verbose_name = "Employee"
        verbose_name_plural = "Employees"


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer")
    registration_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["id"]
        db_table = "Customers"
        managed = True
        verbose_name = "Customer"
        verbose_name_plural = "Customers"


class ConfirmationToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user")
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Confirmation Token for User: {self.user.username}"

    def generate_token(self):
        import secrets

        self.token = secrets.token_urlsafe(nbytes=32)
        return self.token

    def is_valid(self):
        if not self.expires_at:
            return True
        return self.created_at < self.expires_at

    class Meta:
        ordering = ["id"]
        db_table = "ConfirmationTokens"
        managed = True
        verbose_name = "Confirmation Token"
        verbose_name_plural = "Confirmation Tokens"




#
class Category(models.Model):
    category_name = models.CharField(max_length=255, null=False)
    description = models.TextField(null=False, default="")
    parent_category = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="sub_categories",
    )

    def __str__(self):
        return self.category_name

    def clean(self):
        # Check if the parent category is a subcategory
        if self.parent_category:
            if self.parent_category.parent_category:
                raise ValidationError(
                    "Subcategories cannot have subcategories as parent categories."
                )

    def save(self, *args, **kwargs):
        self.full_clean()  # Validate the instance before saving
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["id"]
        db_table = "Categories"
        managed = True
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class Discount(models.Model):
    code = models.CharField(max_length=20, null=True)
    description = models.TextField(blank=True)
    discount_type = models.CharField(
        choices=DISCOUNT_TYPE, default="percentage", null=False
    )
    discount_value = models.DecimalField(max_digits=7, decimal_places=2,null=False,default=0.00)
    applies_to = models.CharField(max_length=20, choices=APPLIES_TO_CHOICES,default='all_products')
    category_id = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)  # Assuming a categories model
    valid_from = models.DateTimeField(default=timezone.now)
    valid_to = models.DateTimeField(blank=True, null=True)
    minimum_purchase = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["id"]
        db_table = "Discounts"
        managed = True
        verbose_name = "Discount"
        verbose_name_plural = "Discounts"

class Brand(models.Model):
    brand_name = models.CharField(max_length=100, null=False)
    contact_person = models.CharField(max_length=100, null=False, default="")
    email = models.EmailField(max_length=100, null=False)
    phone = models.CharField(max_length=15, help_text="Enter your phone number")

    def __str__(self):
        return self.brand_name

    class Meta:
        ordering = ["id"]
        db_table = "Brands"
        managed = True
        verbose_name = "Brand"
        verbose_name_plural = "Brands"


class Product(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255, null=False)
    categories = models.ManyToManyField(Category, related_name="products")
    price = models.IntegerField(null=False, default=0)
    stock_quantity = models.IntegerField(null=False, default=0)
    origin_country = models.CharField(max_length=40, default="")
    information = models.TextField(null=True)
    create_date = models.DateTimeField(default=timezone.now)
    expiry_date = models.DateTimeField(blank=True,null=True)
    sku = models.CharField(max_length=10, unique=True, default="",blank=True)
    unit = models.CharField(choices=UNIT, default="unit")
    is_active = models.BooleanField(default=True)

    inventory_manager = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="managed_product",
    )

    def __str__(self):
        return self.product_name

    def generate_unique_sku(self):
        while True:
            sku = random.randint(1, 999999)
            sku = f"{sku:06}"
            sku = "SP" + sku
            if not Product.objects.filter(sku=sku).exists():
                return sku

    def save(self, *args, **kwargs):
        self.sku = self.generate_unique_sku()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["id"]
        db_table = "Products"
        managed = True
        verbose_name = "Product"
        verbose_name_plural = "Products"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(
        upload_to="images/product_images/", default="images/default/default_fruit.jpg"
    )

    class Meta:
        db_table = "ProductImages"
        managed = True
        verbose_name = "ProductImage"
        verbose_name_plural = "ProductImages"

class SingletonModel(models.Model):
    def save(self,*args, **kwargs):
        self.pk = 1
        return super().save(*args, **kwargs)

class WebsiteInfo(SingletonModel):
    email = models.EmailField(max_length=255, validators=[EmailValidator()],null=False,default='groceryshop@example.com')
    phone = models.CharField(max_length=20, null=False, default="")
    address = models.CharField(max_length=255)
    
    class Meta:
        
        db_table = "WebsiteInfos"
        managed = True
        verbose_name = "Website Infomation"
        verbose_name_plural = "Website Infomations"

class WebsiteImage(models.Model):
    IMAGE_TYPES = (
        ('banner', 'Banner Image'),
        ('slide', 'Slide Image'),
        ('category', 'Category Image'),
        ('about', 'About Image'),
        
    )
    
    image = models.ImageField(upload_to="images/website_images/")
    image_type = models.CharField(max_length=20, choices=IMAGE_TYPES,help_text="Slide:(1342*932); Category:(354*354); About:(540*472)")
    website_info = models.ForeignKey(WebsiteInfo, on_delete=models.CASCADE, related_name='images')

    class Meta:
        
        db_table = "WebsiteImages"
        managed = True
        verbose_name = "Website Image"
        verbose_name_plural = "Website Images"

class Address(models.Model):
    ADDRESS_TYPE = (("home", "Home"), ("office", "Office"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, null=True, blank=True
    )
    full_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True)
    street_address = models.CharField(max_length=255)
    locality = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=100,null=True, blank=True)
    type = models.CharField(max_length=50, choices=ADDRESS_TYPE, default="home")  # Home, Work, Other
    is_default = models.BooleanField(default=False)

    class Meta:
        ordering = ["id"]
        db_table = "Addresses"
        managed = True
        verbose_name = "Address"
        verbose_name_plural = "Addresses"
        constraints = [
            models.UniqueConstraint(fields=["user", "is_default"], name="unique_default_address_per_user"),  # Ensures only one default address per user
        ]

    

class Order(models.Model):
    ORDER_STATUS = (
        ("pending", "Pending"),
        ("complete", "Complete"),
        ("refunded", "Refunded"),
        ("failed", "Failed"),
        ("shipped", "Shipped"),
        ("cancelled", "Cancelled"),
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    placed_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(choices=ORDER_STATUS, null=False,default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    billing_address = models.ForeignKey(Address, on_delete=models.SET_NULL, related_name="billing_orders", null=True, blank=True)
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, related_name="shipping_orders", null=True, blank=True)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD, default="")
    payment_transaction = models.CharField(max_length=255, null=True, blank=True)  # Optional for storing transaction ID
    class Meta:
        ordering = ["-placed_at"]
        db_table = "Orders"
        managed = True
        verbose_name = "Order"
        verbose_name_plural = "Orders"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(null=False, default=0)
    subtotal = models.IntegerField(null=False, default=0)
    discount_applied = models.CharField(max_length=30, default="", null=False)

    class Meta:
        ordering = ["id"]
        db_table = "OrderItems"
        managed = True
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"


class Transaction(models.Model):
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    transaction_date = models.DateTimeField(default=timezone.now)
    payment_method = models.CharField(choices=PAYMENT_METHOD, null=False,default='cash')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default=0.00)

    # transaction_type
    class Meta:
        ordering = ["id"]
        db_table = "Transactions"
        managed = True
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"



class StoreLocation(models.Model):
    location_name = models.CharField(max_length=50, default="", null=False)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)
    manager = models.ForeignKey(Employee, on_delete=models.CASCADE)

    class Meta:
        ordering = ["id"]
        db_table = "StoreLocations"
        managed = True
        verbose_name = "Store Location"
        verbose_name_plural = "Store Locations"


