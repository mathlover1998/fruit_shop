from django.contrib import admin
import django.apps
from django import forms
from django.contrib.auth.models import Group
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import *

#register Product section
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
