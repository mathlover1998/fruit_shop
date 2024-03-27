from django import forms
from django.forms.widgets import TextInput,Select,NumberInput,Textarea,DateInput
from fruit_shop_app.models import Fruit,Category


class CreateFruitForm(forms.ModelForm):
    fruit_name = forms.CharField(
        widget=TextInput(attrs={"placeholder": "Enter Fruit Name"})
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), widget=Select(attrs={"class": "custom-select"}),
        
    )
    price = forms.IntegerField(
        widget=NumberInput(attrs={"min": 0})
    )  # Set minimum price to 0
    stock_quantity = forms.IntegerField(
        widget=NumberInput(attrs={"min": 0})
    )  # Set minimum stock to 0
    origin_country = forms.CharField(
        widget=TextInput(attrs={"placeholder": "Enter Origin Country"})
    )
    nutritional_information = forms.CharField(
        widget=Textarea(attrs={"rows": 4})
    )  # Multiline text input
    expiry_date = forms.DateField(
        widget=DateInput(attrs={"type": "date"})
    )  # Date picker input

    class Meta:
        model = Fruit
        fields = [
            "fruit_name",
            "fruit_image",
            "category",
            "price",
            "stock_quantity",
            "origin_country",
            "nutritional_information",
            "expiry_date",
        ]
