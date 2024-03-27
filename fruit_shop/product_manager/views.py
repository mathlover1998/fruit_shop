from django.shortcuts import render, HttpResponse, redirect
from fruit_shop_app.models import Fruit, Supplier
from django.urls import reverse
from fruit_shop.utils import position_required
from .forms import CreateFruitForm
from django.contrib.auth.decorators import login_required

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
    return render(request, "shop/shop.html")


def fruit_view(request):
    fruit_list = Fruit.objects.all()
    return render(request, "shop/fruits.html", {"fruits": fruit_list})


@login_required
@position_required("inventory_manager", "store_manager")
def create_fruit(request):
    form = CreateFruitForm()
    if request.method == "POST":
        form = CreateFruitForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.inventory_manager = request.user.employee
            form.save()
            return redirect(reverse("fruit_view"))
    return render(request, "shop/create_fruit.html", {"form": form})
