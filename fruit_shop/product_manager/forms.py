from django import forms
from fruit_shop_app.models import Category, Supplier, Employee


class CreateProductForm(forms.Form):

    supplier = forms.ModelChoiceField(
        queryset=Supplier.objects.all(),
        label="Supplier",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    product_name = forms.CharField(
        max_length=255,
        label="Product Name",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    product_image = forms.ImageField(
        label="Product Image",
        widget=forms.FileInput(attrs={"class": "form-control"}),
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label="Category",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    price = forms.IntegerField(
        label="Price", widget=forms.NumberInput(attrs={"class": "form-control"})
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
    create_date = forms.DateField(
        label="Create Date",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
    )
    expiry_date = forms.DateField(
        label="Expiry Date",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        required=False,
    )
