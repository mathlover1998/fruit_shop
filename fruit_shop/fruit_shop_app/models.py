from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    MaxLengthValidator,
    MinLengthValidator,
)

# Create your models here.
GENDER = (("male", "Male"), ("female", "Female"), ("other", "Other"))

POSITION = (
    ("employee", "Employee"),
    ("seller", "Seller"),
    ("store_manager", "Store Manager"),
    ("assistant_manager", "Assistant Manager"),
    ("cashier", "Cashier"),
)
PAYMENT_STATUS = (
    ("pending", "Pending"),
    ("complete", "Complete"),
    ("refunded", "Refunded"),
    ("failed", "Failed"),
    ("abandoned", "Abandoned"),
    ("on_hold", "On Hold"),
    ("cancelled", "Cancelled"),
)

PAYMENT_METHOD = (
    ("cash", "Cash"),
    ("momo", "Momo"),
    ("apple_pay", "Apple Pay"),
    ("mobile_banking", "Mobile Banking"),
)

RECEIVER_TYPE = (("home", "Home"), ("office", "Office"))


class User(AbstractUser):
    phone = models.CharField(max_length=20, null=True)
    middle_name = models.CharField(max_length=255, null=False, default="")
    gender = models.CharField(
        max_length=20, choices=GENDER, default="other", null=False
    )
    dob = models.DateField(default="2000-01-01")
    image = models.ImageField(upload_to="images/", default="images/default-avatar.png")
    receive_updates = models.BooleanField(default=False)

    def get_full_name(self):
        full_name = f"{self.first_name}"
        full_name += " "
        if self.middle_name:
            full_name += " "
            full_name += f"{self.middle_name}"
            full_name += " "
        full_name += f"{self.last_name}"
        return full_name

    class Meta:
        managed = True
        db_table = "Users"
        verbose_name = "User Table"
        verbose_name_plural = "Users Table"
        indexes = [
            models.Index(
                fields=["first_name", "middle_name", "last_name"], name="full_name"
            )
        ]


class Employee(models.Model):
    hire_date = models.DateField(null=False)
    salary = models.IntegerField(null=False, default=0)
    department = models.CharField(max_length=200, default="", null=False)
    position = models.CharField(
        max_length=200, choices=POSITION, default="employee", null=False
    )
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
    discount_code = models.CharField(max_length=20, null=False)
    discount_percentage = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)], null=False
    )
    valid_from = models.DateField(null=False)
    valid_to = models.DateField(null=False)
    min_purchase_amount = models.IntegerField(null=False, default=0)

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

    class Meta:
        ordering = ["id"]
        db_table = "Categories"
        managed = True
        verbose_name = "Category Table"
        verbose_name_plural = "Categories Table"


class Fruit(models.Model):
    fruit_name = models.CharField(max_length=255, null=False)
    fruit_image = models.ImageField(
        upload_to="images/", default="images/default_fruit.jpg"
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField(null=False, default=0)
    stock_quantity = models.IntegerField(null=False, default=0)
    origin_country = models.CharField(max_length=40, default="")
    nutritional_information = models.TextField(null=True)
    create_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField(null=True)

    class Meta:
        ordering = ["id"]
        db_table = "Fruits"
        managed = True
        verbose_name = "Fruit Table"
        verbose_name_plural = "Fruits Table"


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


class Supplier(models.Model):
    supplier_name = models.CharField(max_length=100, null=False)
    contact_person = models.CharField(max_length=100, null=False,default='')
    email = models.EmailField(max_length=100, null=False)
    phone = models.CharField(max_length=15, help_text="Enter your phone number")

    class Meta:
        ordering = ["id"]
        db_table = "Suppliers"
        managed = True
        verbose_name = "Supplier Table"
        verbose_name_plural = "Suppliers Table"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    fruit = models.ForeignKey(Fruit, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(null=False, default=0)
    subtotal = models.IntegerField(null=False, default=0)
    discount_applied = models.CharField(max_length=30, default="", null=False)

    class Meta:
        ordering = ["id"]
        db_table = "OrderItems"
        managed = True
        verbose_name = "Order Item Table"
        verbose_name_plural = "Order Items Table"


class SupplierProduct(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    fruit = models.ForeignKey(Fruit, on_delete=models.CASCADE)
    supplier_product_image = models.ImageField(
        upload_to="images/", default="images/default_can.jpg"
    )
    supply_price = models.FloatField(null=False, default=0.0)
    last_supply_date = models.DateField(null=False)
    quantity_supplied = models.IntegerField(null=False, default=0)

    class Meta:
        ordering = ["id"]
        db_table = "SupplierProducts"
        managed = True
        verbose_name = "Supplier Product Table"
        verbose_name_plural = "Supplier Products Table"


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
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, null=True, blank=True
    )
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, null=True, blank=True
    )
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

    # Tỉnh (Province), Quận (District):Phường (Ward):Xã (Commune):
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
