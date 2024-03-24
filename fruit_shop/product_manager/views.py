from django.shortcuts import render,HttpResponse
from fruit_shop_app.models import Fruit

# Create your views here.
def product_view(request):
    return render(request,'shop/shop.html')


def create_fruit(request):
    return render (request,'shop/fruits.html')