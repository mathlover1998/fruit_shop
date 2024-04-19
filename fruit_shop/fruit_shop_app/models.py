from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
import random
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Permission
from django.utils.translation import gettext_lazy as _

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
PAYMENT_STATUS = (
    ("pending", "Pending"),
    ("complete", "Complete"),
    ("refunded", "Refunded"),
    ("failed", "Failed"),
    ("abandoned", "Abandoned"),
    ("on_hold", "On Hold"),
    ("cancelled", "Cancelled"),
)
UNIT = (
    ("kg", "Kilogram"),
    ("gr", "Gram"),
    ("set", "Set"),
    ("pack", "Pack"),
    ("unit", "Unit"),
)
PAYMENT_METHOD = (("cash", "Cash"), ("momo", "Momo"))

RECEIVER_TYPE = (("home", "Home"), ("office", "Office"))

DISCOUNT_TYPE = (("percentage", "Percentage"), ("fixed_discount", "Fixed Discount"))


class User(AbstractUser):
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
        verbose_name = "User Table"
        verbose_name_plural = "Users Table"
        indexes = [models.Index(fields=["first_name", "last_name"], name="full_name")]


class Position(models.Model):
    name = models.CharField(_("Name"), max_length=100, unique=True)
    permissions = models.ManyToManyField(Permission, blank=True)

    class Meta:
        verbose_name = _("Position")
        verbose_name_plural = _("Positions")

    def __str__(self):
        return self.name


class Employee(models.Model):
    hire_date = models.DateField(null=True)
    salary = models.IntegerField(null=False, default=0)
    department = models.CharField(max_length=200, default="", null=False)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employee")

    class Meta:
        ordering = ["id"]
        db_table = "Employees"
        managed = True
        verbose_name = "Employee Table"
        verbose_name_plural = "Employees Table"


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer")
    registration_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["id"]
        db_table = "Customers"
        managed = True
        verbose_name = "Customer Table"
        verbose_name_plural = "Customers Table"


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
        verbose_name = "Confirmation Token Table"
        verbose_name_plural = "Confirmation Tokens Table"


class Discount(models.Model):
    min_purchase_amount = models.IntegerField(null=False, default=0)
    is_active = models.BooleanField(default=True)
    discount_type = models.CharField(
        choices=DISCOUNT_TYPE, default="percentage", null=False
    )
    amount_of_use = models.IntegerField(
        null=False, validators=[MinValueValidator(1)], default=1
    )
    discount_code = models.CharField(max_length=20, null=True)
    discount_percentage = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)], null=True
    )
    max_value_discount = models.FloatField(null=False, default=0)
    valid_from = models.DateField(null=True)
    valid_to = models.DateField(null=True)

    class Meta:
        ordering = ["id"]
        db_table = "Discounts"
        managed = True
        verbose_name = "Discount Table"
        verbose_name_plural = "Discounts Table"


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
        verbose_name = "Category Table"
        verbose_name_plural = "Categories Table"


class Supplier(models.Model):
    supplier_name = models.CharField(max_length=100, null=False)
    contact_person = models.CharField(max_length=100, null=False, default="")
    email = models.EmailField(max_length=100, null=False)
    phone = models.CharField(max_length=15, help_text="Enter your phone number")

    def __str__(self):
        return self.supplier_name

    class Meta:
        ordering = ["id"]
        db_table = "Suppliers"
        managed = True
        verbose_name = "Supplier Table"
        verbose_name_plural = "Suppliers Table"


class Product(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255, null=False)
    categories = models.ManyToManyField(Category, related_name="products")
    price = models.IntegerField(null=False, default=0)
    stock_quantity = models.IntegerField(null=False, default=0)
    origin_country = models.CharField(max_length=40, default="")
    information = models.TextField(null=True)
    create_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField(null=True)
    sku = models.CharField(max_length=10, unique=True, default="")
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
        verbose_name = "Product Table"
        verbose_name_plural = "Products Table"


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
        verbose_name = "ProductImage Table"
        verbose_name_plural = "ProductImages Table"


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateField(auto_now=True)
    total_amount = models.IntegerField(null=False, default=0)
    payment_status = models.CharField(choices=PAYMENT_STATUS, null=False)
    delivery_address = models.CharField(max_length=255, default="", null=False)
    delivery_date = models.DateField(null=True)

    class Meta:
        ordering = ["id"]
        db_table = "Orders"
        managed = True
        verbose_name = "Order Table"
        verbose_name_plural = "Orders Table"


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
        verbose_name = "Order Item Table"
        verbose_name_plural = "Order Items Table"


class Transaction(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    transaction_date = models.DateField(auto_now=True)
    payment_method = models.CharField(choices=PAYMENT_METHOD, null=False)
    amount_paid = models.FloatField(null=False, default=0.0)

    # transaction_type
    class Meta:
        ordering = ["id"]
        db_table = "Transactions"
        managed = True
        verbose_name = "Transaction Table"
        verbose_name_plural = "Transactions Table"


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    supplier = models.ForeignKey(
        Supplier, on_delete=models.CASCADE, null=True, blank=True
    )
    receiver_name = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(max_length=20, null=True)
    street = models.CharField(max_length=255, default="", null=False)
    commune = models.CharField(max_length=50, default="", null=True)
    ward = models.CharField(max_length=50, default="", null=True)
    district = models.CharField(max_length=50, default="", null=True)
    province = models.CharField(max_length=50, default="", null=True)
    country = models.CharField(max_length=50, default="", null=False)
    zipcode = models.IntegerField(null=False, default=0)
    type = models.CharField(choices=RECEIVER_TYPE, default="home", null=False)
    default_address = models.BooleanField(default=False)

    class Meta:
        ordering = ["id"]
        db_table = "Addresses"
        managed = True
        verbose_name = "Address Table"
        verbose_name_plural = "Addresses Table"


class StoreLocation(models.Model):
    location_name = models.CharField(max_length=50, default="", null=False)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)
    manager = models.ForeignKey(Employee, on_delete=models.CASCADE)

    class Meta:
        ordering = ["id"]
        db_table = "StoreLocations"
        managed = True
        verbose_name = "Store Location Table"
        verbose_name_plural = "Store Locations Table"

