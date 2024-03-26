from django.shortcuts import render,HttpResponse,redirect
from fruit_shop_app.models import Fruit,Supplier
from django.urls import reverse

# Create your views here.

def supplier_register(request):
    if request.method == "POST":
        supplier_name = request.POST.get("supplier_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        new_supplier = Supplier.objects.create(
            supplier_name=supplier_name, email=email, phone=phone
        )
        new_supplier.save()
        return redirect(reverse("confirmation_page"))
    return render(request, "account/supplier_register.html")


def confirmation_page(request):
    return render(request, "notification/wait_for_confirmation.html")


def product_view(request):
    return render(request,'shop/shop.html')


def create_fruit(request):
    return render (request,'shop/fruits.html')