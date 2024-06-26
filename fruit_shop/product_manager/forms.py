from django import forms
from fruit_shop_app.models import Category, Brand, Employee,UNIT

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ProductForm(forms.Form):

    brand = forms.ModelChoiceField(
        queryset=Brand.objects.all(),
        label="Brand",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    product_name = forms.CharField(
        max_length=255,
        label="Product Name",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    product_images = MultipleFileField(
        label="Product Images",
        required=False,
    )
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.filter(type='product',parent_category__isnull=False),
        label="Categories",
        widget=forms.SelectMultiple(attrs={"class": "form-control"})
    )
    price = forms.IntegerField(
        label="Price (VND)", widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    unit = forms.ChoiceField(
        choices=UNIT,
        label="Unit",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    stock_quantity = forms.IntegerField(
        label="Stock Quantity",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    origin_country = forms.CharField(
        max_length=40,
        label="Origin Country",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    information = forms.CharField(
        label="Information",
        widget=forms.Textarea(
            attrs={"class": "form-control", "rows": 3}
        ),  # Using Textarea widget
        required=False,
    )
