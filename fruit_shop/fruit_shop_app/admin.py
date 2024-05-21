from collections.abc import Sequence
from typing import Any
from django.contrib import admin
import django.apps
from django import forms
from django.contrib.auth.models import Group, Permission
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.fields.related import ForeignKey
from django.db.models.query import QuerySet
from django.http import HttpRequest
from .models import *
from django.utils.translation import gettext_lazy as _

admin.site.register(Permission)

# filter to get the most product sold
# filter to get the most category that have all products sold


# filter email (has email, no email)

class PriceRangeFilter(admin.SimpleListFilter):
    title = _('price range')
    parameter_name = 'price_range'

    def lookups(self, request, model_admin):
        return (
            ('0-100', _('0 to 100')),
            ('101-500', _('101 to 500')),
            ('501-1000', _('501 to 1000')),
            ('1000+', _('1000+')),
        )

    def queryset(self, request, queryset):
        if self.value() == '0-100':
            return queryset.filter(price__gte=0, price__lte=100000)
        if self.value() == '101-500':
            return queryset.filter(price__gte=100001, price__lte=500000)
        if self.value() == '501-1000':
            return queryset.filter(price__gte=500001, price__lte=1000000)
        if self.value() == '1000+':
            return queryset.filter(price__gte=1001)
        return queryset

class EmailFilter(admin.SimpleListFilter):
    title = _(
        "Email Filter",
    )
    parameter_name = "email"

    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        return (("has_email", _("Has Email")), ("no_email", _("No Email")))

    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if not self.value():
            return queryset
        if self.value().lower() == "has_email":
            return queryset.exclude(email="")
        if self.value().lower() == "no_email":
            return queryset.filter(email="")


# filter phone number (has phone, no phone)
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
    list_filter = ["is_superuser", "date_joined", EmailFilter]
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
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'categories':
            kwargs['queryset'] = Category.objects.filter(type='product',parent_category__isnull=False)
        return super().formfield_for_manytomany(db_field, request, **kwargs)
    inlines = [ProductImageInline]
    form = ProductForm
    search_fields = ["product_name", "sku"]
    list_display = ['product_name','sku','price','brand','is_featured','is_active']
    list_per_page = 20
    list_filter = ["is_active", PriceRangeFilter, "stock_quantity"]
    readonly_fields = ["create_date",'updated_price','updated_at']
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
                    ("price",'updated_price', "unit"),
                    "stock_quantity",
                    ("categories", "brand"),
                    "is_featured",
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
                    ("create_date", "updated_at"),
                ),
            },
        ),
    )

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == "inventory_manager":
    #         kwargs["queryset"] = Employee.objects.select_related("user")  # Optimize query
    #         kwargs["label_from_instance"] = lambda obj: obj.user.username  # Display username
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)


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
        self.fields["maximum_discount_amount"].help_text = (
            "The maximum value to reduce"
        )
        self.fields["minimum_purchase"].help_text = (
            "Minimum purchase amount required to qualify for the discount"
        )
        self.fields["category"].help_text = (
            "Select category if and only if applies_to be selected as Category"
        )
        self.fields["brand"].help_text = (
            "Select brand if and only if applies_to be selected as Brand"
        )
        self.fields["products"].help_text = (
            "Select products if and only if applies_to be selected as Product"
        )
    

    class Meta:
        model = Discount
        # exclude some fields we do not want
        exclude = ()


class DiscountAdmin(admin.ModelAdmin):
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'products':
            # Filter products based on the current logged-in account (inventory_manager)
            kwargs['queryset'] = request.user.employee.managed_product.all()
        return super().formfield_for_manytomany(db_field, request, **kwargs)
    
    form = DiscountForm
    list_display = ("code", "discount_type","applies_to", "valid_from", "valid_to", "is_active")
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
                    'maximum_discount_amount',
                    "minimum_purchase",
                    "is_active",
                    ("valid_from", "valid_to"),
                    "applies_to",
                    "category",
                    'brand',
                    'products',
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
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name== 'parent_category':
            kwargs['queryset'] = Category.objects.filter(parent_category__isnull=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    list_display = ("category_name",)
    search_fields = ("category_name",)
    fieldsets = (
        (
            "Information",
            {"fields": ("category_name","type", "description", "parent_category")},
        ),
    )


admin.site.register(Category, CategoryAdmin)


# Order section
class OrderAdmin(admin.ModelAdmin):
    list_display = ("customer", "placed_at", "status")
    search_fields = ("customer",)
    list_filter = ("placed_at", "status", "payment_method")


admin.site.register(Order, OrderAdmin)


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("user",)


admin.site.register(Employee, EmployeeAdmin)


# Website section
class WebsiteImageInline(admin.TabularInline):
    model = WebsiteImage
    extra = 1
    fields = [
        "image_type",
        "image",
        
    ]


class WebsiteInfoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WebsiteInfoForm, self).__init__(*args, **kwargs)
        self.fields["email"].help_text = "Email of Website"

    class Meta:
        model = WebsiteInfo
        exclude = ("",)


class WebsiteInfoAdmin(admin.ModelAdmin):
    list_display = ("email",)
    form = WebsiteInfoForm
    inlines = [WebsiteImageInline]
    fieldsets = (
        (
            "Information",
            {
                "fields": (
                    "email",
                    "phone",
                    'address',
                ),
            },
        ),
    )
    
admin.site.register(WebsiteInfo, WebsiteInfoAdmin)

#category and product many to many model section


#comment section
class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields["content"].help_text = "Content of comment"
        
    class Meta:
        model = Comment
        exclude = ("",)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['user','is_approved',]
    form = CommentForm
    readonly_fields = ['created_at','updated_at']
    fieldsets = (
        (
            "Information",
            {
                "fields": (
                    "content",
                    "user",
                    "parent_comment",
                    ("created_at","updated_at"),
                    'product',
                    'is_approved'
                ),
            },
        ),
    )
    has_add_permission = lambda self, request: False

admin.site.register(Comment,CommentAdmin)

@admin.register(ContactUsMessage)
class ContactUsMessageAdmin(admin.ModelAdmin):
    list_display = ['name','email',]
    fieldsets = (
        (
            "Information",
            {
                "fields": (
                    "name",
                    "email",
                    "subject",
                    'content'
                ),
            },
        ),
    )
    has_add_permission = lambda self, request: False


# models = django.apps.apps.get_models()
# for model in models:
#     try:
#         admin.site.register(model)
#     except admin.sites.AlreadyRegistered:
#         pass
