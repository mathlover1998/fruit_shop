from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import (
    User,
    Category,
    Product,
    Employee,
    Customer,
    Order,
    OrderItem,
    Supplier,
    Transaction,
    Discount,
    StoreLocation,
    Address,
    ProductImage,
    DISCOUNT_TYPE,
    Position

)


admin.site.register(User)
admin.site.register(Category)
admin.site.register(Employee)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Supplier)
admin.site.register(Transaction)
admin.site.register(StoreLocation)
admin.site.register(Address)
admin.site.register(Position)



class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

admin.site.register(Product, ProductAdmin)


class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        exclude = ()

    discount_type = forms.ChoiceField(
        choices=DISCOUNT_TYPE, widget=forms.RadioSelect(attrs={'class': 'discount-type-radio'})
    )
    discount_percentage = forms.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        widget=forms.NumberInput(attrs={'class': 'discount-percentage-input'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['discount_percentage'].widget.attrs['readonly'] = True  # Set readonly attribute for better UX

        # Enable the field conditionally based on discount_type
        if self.initial.get('discount_type') == 'percentage':
            self.fields['discount_percentage'].disabled = False
            self.fields['discount_percentage'].widget.attrs.pop('readonly')  # Remove readonly attribute


class DiscountAdmin(admin.ModelAdmin):
    form = DiscountForm
    list_display = (
        'min_purchase_amount', 'is_active', 'get_discount_type_display', 'amount_of_use', 'discount_code',
        'discount_percentage', 'max_value_discount', 'valid_from', 'valid_to')
    search_fields = ('discount_code',)
    list_filter = ('is_active', 'valid_from', 'valid_to')
    ordering = ('-valid_from',)

    class Media:
        js = ('admin_custom.js',)


admin.site.register(Discount, DiscountAdmin)