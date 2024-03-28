from django import forms
from django.forms.widgets import TextInput, Select, NumberInput, Textarea, DateInput
from fruit_shop_app.models import Fruit, Category, SupplierProduct, Supplier


class CreateFruitForm(forms.Form):
    fruit_name = forms.CharField(
        label="Fruit Name",  # Specify the label here
        widget=forms.TextInput(
            attrs={"placeholder": "Enter Fruit Name", "class": "form-control"}
        ),
    )
    category = forms.ModelChoiceField(
        label="Category",  # Specify the label here
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={"class": "custom-select form-control"}),
    )
    price = forms.IntegerField(
        label="Price",  # Specify the label here
        widget=forms.NumberInput(attrs={"min": 0, "class": "form-control"}),
    )
    stock_quantity = forms.IntegerField(
        label="Stock Quantity",  # Specify the label here
        widget=forms.NumberInput(attrs={"min": 0, "class": "form-control"}),
    )
    origin_country = forms.CharField(
        label="Origin Country",  # Specify the label here
        widget=forms.TextInput(
            attrs={"placeholder": "Enter Origin Country", "class": "form-control"}
        ),
    )
    nutritional_information = forms.CharField(
        label="Nutritional Information",  # Specify the label here
        widget=forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
    )
    expiry_date = forms.DateField(
        label="Expiry Date",  # Specify the label here
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
    )
    fruit_image = forms.ImageField(
        label="Fruit Imageeeee",  # Specify the label here
        required=False,
        widget=forms.FileInput(attrs={"class": "form-control"}),
    )


class CreateProductForm(forms.Form):
    fruit = forms.ModelChoiceField(
        queryset=Fruit.objects.all(),
        label="Fruit",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    supplier = forms.ModelChoiceField(
        queryset=Supplier.objects.all(),
        label="Supplier",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    supplier_product_image = forms.ImageField(
        label="Supplier Product Image",
        required=False,
        widget=forms.FileInput(attrs={"class": "form-control"}),
    )
    supply_price = forms.FloatField(
        label="Supply Price", widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    last_supply_date = forms.DateField(
        label="Last Supply Date",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
    )
    quantity_supplied = forms.IntegerField(
        label="Quantity Supplied",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
