from collections.abc import Sequence
from typing import Any
from django.contrib import admin
import django.apps
from django import forms
from django.contrib.auth.models import Group, Permission
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.query import QuerySet
from django.http import HttpRequest
from .models import *
from django.utils.translation import gettext_lazy as _

admin.site.register(Permission)

#filter to get the most product sold
#filter to get the most category that have all products sold


#filter email (has email, no email)
class EmailFilter(admin.SimpleListFilter):
    title = _('Email Filter',)
    parameter_name = 'email'

    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        return (
            ('has_email',_('Has Email')),
            ('no_email',_('No Email'))
        )

    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if not self.value():
            return queryset
        if self.value().lower() == 'has_email':
            return queryset.exclude(email = '')
        if self.value().lower() == 'no_email':
            return queryset.filter(email='')

#filter phone number (has phone, no phone)
class PhoneFilter(admin.SimpleListFilter):
    title = _()
    pass
# User section
class AddressInline(admin.TabularInline):
    model = Address
    extra = 1
    fields = ["full_name", "phone_number", "street_address", "is_default"]


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
    list_filter = ["is_superuser", "date_joined",EmailFilter]
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


# Product section
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
    search_fields = ["product_name", "sku"]
    list_per_page = 20
    list_filter = ["is_active", "price", "stock_quantity"]
    readonly_fields = ["create_date"]
    ordering = [
        "-create_date",
    ]
    fieldsets = (
        (
            "Main Information",
            {
                "fields": (
                    ("product_name", "sku"),
                    "inventory_manager",
                    ("price", "unit"),
                    "stock_quantity",
                    ("categories", "supplier"),
                    "is_active",
                ),
            },
        ),
        (
            "More Information",
            {
                "fields": (
                    "origin_country",
                    "information",
                    ("create_date", "expiry_date"),
                ),
            },
        ),
    )


admin.site.register(Product, ProductFormAdmin)


# Discount Section
class DiscountForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DiscountForm, self).__init__(*args, **kwargs)
        self.fields["code"].help_text = "Discount Code"
        self.fields["discount_value"].help_text = (
            "Between 0.01 and 1 if percentage option is selected"
        )
        self.fields["applies_to"].help_text = (
            "Defines what the discount applies to (all products, specific category, or specific products)."
        )
        self.fields["minimum_purchase"].help_text = (
            "Minimum purchase amount required to qualify for the discount"
        )
        self.fields["category_id"].help_text = (
            "select category if and only if applies_to be selected as Category"
        )

    class Meta:
        model = Discount
        # exclude some fields we do not want
        exclude = ()


class DiscountAdmin(admin.ModelAdmin):
    form = DiscountForm
    list_display = ("code", "discount_type", "valid_from", "valid_to", "is_active")
    search_fields = ("code",)
    list_filter = ("is_active", "valid_from", "valid_to", "discount_type")
    ordering = ("-valid_from",)
    fieldsets = (
        (
            "Information",
            {
                "fields": (
                    "code",
                    "description",
                    ("discount_type", "discount_value"),
                    "minimum_purchase",
                    "is_active",
                    ("valid_from", "valid_to"),
                    "applies_to",
                    "category_id",
                ),
            },
        ),
    )


admin.site.register(Discount, DiscountAdmin)


# Brand section
class BrandAdmin(admin.ModelAdmin):
    list_display = ("brand_name", "phone")
    search_fields = ("brand_name",)
    fieldsets = (
        (
            "Information",
            {
                "fields": (
                    "brand_name",
                    "contact_person",
                    "email",
                    "phone",
                ),
            },
        ),
    )


admin.site.register(Brand, BrandAdmin)



# Category Section
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("category_name",)
    search_fields = ("category_name",)
    fieldsets = (
        (
            "Information",
            {"fields": ("category_name", "description", "parent_category")},
        ),
    )


admin.site.register(Category, CategoryAdmin)

#Order section
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer','placed_at','status')
    search_fields = ('customer',)
    list_filter = ('placed_at','status','payment_method')


admin.site.register(Order,OrderAdmin)

# models = django.apps.apps.get_models()
# for model in models:
#     try:
#         admin.site.register(model)
#     except admin.sites.AlreadyRegistered:
#         pass
