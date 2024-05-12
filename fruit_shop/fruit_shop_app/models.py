from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator, EmailValidator
import random
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth.models import Permission
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
from django.utils import timezone

# Create your models here.
GENDER = (("male", "Male"), ("female", "Female"), ("other", "Other"))


UNIT = (
    ("kg", "Kilogram"),
    ("gr", "Gram"),
    ("set", "Set"),
    ("pack", "Pack"),
    ("unit", "Unit"),
)


PAYMENT_METHOD = (("cash", "Cash"), ("momo", "Momo"))


class User(AbstractUser, PermissionsMixin):
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
    # groups = models.ManyToManyField(
    #     Group,
    #     blank=True,
    #     related_name="user_memberships",  # Specify a unique related_name
    # )

    def save(self, *args, **kwargs):
        if not self.pk and not self.password:
            self.set_password("012198218")
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
    CATEGORY_TYPE = (('product','Product'),('blog','Blog'))
    category_name = models.CharField(max_length=255, unique=True)
    type = models.CharField(choices=CATEGORY_TYPE,default='product')
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


class Brand(models.Model):
    brand_name = models.CharField(max_length=100, unique=True)
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
    updated_price = models.IntegerField(null=False, default=0)
    stock_quantity = models.IntegerField(null=False, default=0)
    origin_country = models.CharField(max_length=40, default="")
    information = models.TextField(null=True)
    create_date = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    expiry_date = models.DateTimeField(blank=True, null=True)
    sku = models.CharField(max_length=10, unique=True, default="", blank=True)
    unit = models.CharField(choices=UNIT, default="unit")
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    inventory_manager = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="managed_product",
    )

    def apply_discount(self, discount):
        if discount.discount_type == "percentage":
            discount_amount = self.price * discount.discount_value
        elif discount.discount_type == "fixed_amount":
            discount_amount = discount.discount_value

        discount_amount = min(discount_amount, discount.maximum_discount_amount)
        self.updated_price = self.price - discount_amount
        self.save()

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
        if self.updated_price == 0:  # Check if updated_price is not already set
            self.updated_price = self.price
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
    is_main_image = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not ProductImage.objects.filter(product=self.product).exists():
            self.is_main_image = True
        else:
            if self.is_main_image:
                ProductImage.objects.filter(product=self.product).exclude(pk=self.pk).update(is_main_image=False)
        super().save(*args, **kwargs)


    class Meta:
        db_table = "ProductImages"
        managed = True
        verbose_name = "ProductImage"
        verbose_name_plural = "ProductImages"
        


class Discount(models.Model):
    DISCOUNT_TYPE = (("percentage", "Percentage"), ("fixed_amount", "Fixed Amount"))
    APPLIES_TO_CHOICES = (
        ("all_products", "All Products"),
        ("category", "Category"),
        ("specific_products", "Specific Products"),
        ("brand", "Brand"),
    )
    code = models.CharField(max_length=20, null=True)
    description = models.TextField(blank=True)
    discount_type = models.CharField(
        choices=DISCOUNT_TYPE, default="percentage", null=False
    )
    discount_value = models.DecimalField(
        max_digits=7, decimal_places=2, null=False, default=0.00
    )
    applies_to = models.CharField(
        max_length=20, choices=APPLIES_TO_CHOICES, default="all_products"
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, blank=True, null=True
    )  # Assuming a categories model
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, blank=True, null=True)
    products = models.ManyToManyField(Product, related_name="discounts",blank=True)
    valid_from = models.DateTimeField(default=timezone.now)
    valid_to = models.DateTimeField(blank=True, null=True)
    minimum_purchase = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, null=False
    )
    maximum_discount_amount = models.DecimalField(
        max_digits=8, decimal_places=2, default=0.00, null=False
    )
    is_active = models.BooleanField(default=True)
    def clean(self):
        """
        Custom validation to ensure discount value is within reasonable limits.
        """
        if self.discount_type == "percentage":
            if self.discount_value < 0.00 or self.discount_value > 1:
                raise ValidationError(
                    "Discount value for percentage discounts must be between 0.00 and 1."
                )
        elif self.discount_value < 0:
            raise ValidationError("Discount value cannot be negative.")
        
    def save(self, *args, **kwargs):
        self.clean()  # Run custom validation
        
        super().save(*args, **kwargs)
        if self.applies_to == "category":

            products_to_discount = Product.objects.filter(categories=self.category)

        elif self.applies_to == "brand":
            
            products_to_discount = Product.objects.filter(brand=self.brand)
        elif self.applies_to == "all_products":

            products_to_discount = Product.objects.all()
        elif self.applies_to == "specific_products":
            products_to_discount = Product.objects.filter(discounts__isnull=True)  # Filter products without discounts
            for product in products_to_discount:
                product.apply_discount(self)
            self.products.add(*products_to_discount)
            
            return
        # Apply the discount to selected products
        for product in products_to_discount:
            product.apply_discount(self)
            
        

    class Meta:
        ordering = ["id"]
        db_table = "Discounts"
        managed = True
        verbose_name = "Discount"
        verbose_name_plural = "Discounts"


class SingletonModel(models.Model):
    def save(self, *args, **kwargs):
        self.pk = 1
        return super().save(*args, **kwargs)


class WebsiteInfo(SingletonModel):
    email = models.EmailField(
        max_length=255,
        validators=[EmailValidator()],
        null=False,
        default="groceryshop@example.com",
    )
    phone = models.CharField(max_length=20, null=False, default="")
    address = models.CharField(max_length=255)

    class Meta:

        db_table = "WebsiteInfos"
        managed = True
        verbose_name = "Website Infomation"
        verbose_name_plural = "Website Infomations"


class WebsiteImage(models.Model):
    IMAGE_TYPES = (
        ("instagram", "Instagram Image"),
        ("slide", "Slide Image"),
        ("category", "Category Image"),
        ("about", "About Image"),
    )

    image = models.ImageField(upload_to="images/website_images/")
    image_type = models.CharField(
        max_length=20,
        choices=IMAGE_TYPES,
        help_text="Slide:(1342*932); Category:(354*354); About:(540*472)",
    )
    website_info = models.ForeignKey(
        WebsiteInfo, on_delete=models.CASCADE, related_name="images"
    )

    class Meta:

        db_table = "WebsiteImages"
        managed = True
        verbose_name = "Website Image"
        verbose_name_plural = "Website Images"


class Address(models.Model):
    ADDRESS_TYPE = (("home", "Home"), ("office", "Office"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True)
    street_address = models.CharField(max_length=255)
    locality = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(
        max_length=50, choices=ADDRESS_TYPE, default="home"
    )  # Home, Work, Other
    is_default = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not Address.objects.filter(user=self.user).exists():
            self.is_default = True
        else:
            if self.is_default:
                Address.objects.filter(user=self.user).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)
    class Meta:
        ordering = ["id"]
        db_table = "Addresses"
        managed = True
        verbose_name = "Address"
        verbose_name_plural = "Addresses"
        


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
    status = models.CharField(choices=ORDER_STATUS, null=False, default="pending")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    billing_address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        related_name="billing_orders",
        null=True,
        blank=True,
    )
    shipping_address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        related_name="shipping_orders",
        null=True,
        blank=True,
    )
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD, default="")
    payment_transaction = models.CharField(
        max_length=255, null=True, blank=True
    )  # Optional for storing transaction ID

    def apply_discount(self, discount):
        # Calculate discount amount based on the discount type and value
        if discount.discount_type == "percentage":
            discount_amount = (discount.discount_value / 100) * self.total_amount
        elif discount.discount_type == "fixed_amount":
            discount_amount = min(discount.discount_value, self.total_amount)

        # Update the total amount of the order after applying the discount
        self.total_amount -= discount_amount
        self.save()

        # Optionally, store information about the applied discount
        # For example, you can update the discount_applied field of each order item
        order_items = self.orderitem_set.all()
        for order_item in order_items:
            order_item.discount_applied = discount.code
            order_item.save()

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
    payment_method = models.CharField(
        choices=PAYMENT_METHOD, null=False, default="cash"
    )
    amount_paid = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default=0.00
    )

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

class Tag(models.Model):
    name = models.CharField(max_length=255, null=False)

    class Meta:
        ordering = ["id"]
        db_table = "Tags"
        managed = True
        verbose_name = "Tag"
        verbose_name_plural = "Tags"


class Blog(models.Model):
    title = models.CharField(
        null=False, max_length=100, default="", help_text="Title of blog"
    )
    subtitle = models.CharField(max_length=255, null=False, default="")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blogs")
    date = models.DateField(auto_now_add=True)
    content = models.TextField(null=True)
    slug = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(default=timezone.now)
    categories = models.ManyToManyField(Category, related_name="blogs")
    tags = models.ManyToManyField(Tag, related_name="blogs")

    class Meta:
        ordering = ["id"]
        db_table = "Blogs"
        managed = True
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"


class BlogImage(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(
        upload_to="images/blog_images/", default="images/default/default_fruit.jpg"
    )
    is_main_image = models.BooleanField(default=False)
    def clean(self):
        if self.is_main_image:
            if self.blog.images.filter(is_main_image=True).exclude(pk=self.pk).exists():
                raise ValidationError("Each product can only have one main image.")
    
    def save(self, *args, **kwargs):
        if not BlogImage.objects.filter(blog=self.blog).exists():
            self.is_main_image = True
        else:
            if self.is_main_image:
                BlogImage.objects.filter(blog=self.blog).exclude(pk=self.pk).update(is_main_image=False)
        super().save(*args, **kwargs)

    class Meta:
        db_table = "BlogImages"
        managed = True
        verbose_name = "Blog Image"
        verbose_name_plural = "Blog Images"
        constraints = [
            models.UniqueConstraint(
                fields=["blog", "is_main_image"],
                name="unique_main_image_per_blog",
            )
        ]

class Comment(models.Model):
    user = models.ForeignKey(User,models.CASCADE,null=False,related_name='comments')
    product = models.ForeignKey(Product,null=True,blank=True,on_delete=models.CASCADE,related_name='comments')
    blog = models.ForeignKey(Blog,null=True,blank=True,on_delete=models.CASCADE,related_name='comments')
    content = models.TextField(null=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=True)
    parent_comment = models.ForeignKey('self',null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    
    class Meta:
        ordering = ["id"]
        db_table = "Comments"
        managed = True
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

