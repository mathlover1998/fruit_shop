from collections.abc import Sequence
from django.contrib import admin
import django.apps
from django import forms
from django.contrib.auth.models import Group
from django.core.validators import MinValueValidator, MaxValueValidator
from django.http import HttpRequest
from .models import *


class AddressInline(admin.TabularInline):
    model = Address
    extra = 1
    fields = ["receiver_name", "phone_number", "street", "default_address"]


class EmployeeInline(admin.TabularInline):
    model = Employee


class CustomerInline(admin.TabularInline):
    model = Customer


class UserAdmin(admin.ModelAdmin):
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
    inlines = [AddressInline, CustomerInline, EmployeeInline]
    list_display = [
        "username",
        "email",
        "phone",
        "is_staff",
        "is_active",
        "is_approved",
        "gender",
    ]
    list_filter = ["is_superuser", "date_joined"]
    search_fields = ["username", "email"]
    list_per_page = 20
    readonly_fields = ["date_joined", "last_login", "approval_email_sent"]
    ordering = [
        "-date_joined",
    ]
    fieldsets = (
        (
            "Main Information",
            {
                "fields": (("username"), "email", "password"),
            },
        ),
        (
            "Personal Information",
            {
                "fields": (
                    ("first_name", "last_name"),
                    ("phone"),
                    ("dob", "gender"),
                )
            },
        ),
        (
            "Status and Permissions",
            {
                "fields": (
                    "is_active",
                    "last_login",
                    ("is_superuser", "is_staff"),
                    "date_joined",
                    ("is_approved", "receive_updates", "approval_email_sent"),
                    "groups",
                    "user_permissions",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Image",
            {
                "fields": ("image",),
            },
        ),
    )


admin.site.register(User, UserAdmin)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields["product_name"].help_text = "New Help text"

    class Meta:
        model = Product
        exclude = ("",)


class ProductFormAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    form = ProductForm


admin.site.register(Product, ProductFormAdmin)


class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        # exclude some fields we do not want
        exclude = ()

    discount_type = forms.ChoiceField(
        choices=DISCOUNT_TYPE,
        widget=forms.RadioSelect(attrs={"class": "discount-type-radio"}),
    )
    discount_percentage = forms.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        widget=forms.NumberInput(attrs={"class": "discount-percentage-input"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["discount_percentage"].widget.attrs[
            "readonly"
        ] = True  # Set readonly attribute for better UX

        # Enable the field conditionally based on discount_type
        if self.initial.get("discount_type") == "percentage":
            self.fields["discount_percentage"].disabled = False
            self.fields["discount_percentage"].widget.attrs.pop(
                "readonly"
            )  # Remove readonly attribute


class DiscountAdmin(admin.ModelAdmin):
    form = DiscountForm
    list_display = (
        "min_purchase_amount",
        "is_active",
        "get_discount_type_display",
        "amount_of_use",
        "discount_code",
        "discount_percentage",
        "max_value_discount",
        "valid_from",
        "valid_to",
    )
    search_fields = ("discount_code",)
    list_filter = ("is_active", "valid_from", "valid_to")
    ordering = ("-valid_from",)


admin.site.register(Discount, DiscountAdmin)


models = django.apps.apps.get_models()
for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
