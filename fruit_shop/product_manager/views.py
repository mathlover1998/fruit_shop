from django.shortcuts import render, HttpResponse, redirect
from fruit_shop_app.models import Fruit, Supplier,SupplierProduct
from django.urls import reverse
from fruit_shop.utils import position_required
from .forms import CreateFruitForm,CreateProductForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

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
            fruit_name=form.cleaned_data['fruit_name']
            if Fruit.objects.filter(fruit_name=fruit_name).exists():
                return JsonResponse({'error': 'Fruit name already exists'}, status=400)
            fruit = Fruit(
                    fruit_name=fruit_name,
                    category=form.cleaned_data['category'],
                    price=form.cleaned_data['price'],
                    stock_quantity=form.cleaned_data['stock_quantity'],
                    origin_country=form.cleaned_data['origin_country'],
                    nutritional_information=form.cleaned_data['nutritional_information'],
                    expiry_date=form.cleaned_data['expiry_date'],
                    inventory_manager=request.user.employee
                )
            if 'fruit_image' in  request.FILES:
                fruit.fruit_image=form.cleaned_data['fruit_image'],
            fruit.save()
            return redirect(reverse("fruit_view"))
    return render(request, "shop/create_fruit.html", {"form": form})


@login_required
@position_required("inventory_manager", "store_manager")
def create_product(request):
    form = CreateProductForm()
    if request.method =='POST':
        form = CreateProductForm(request.POST,request.FILES)
        if form.is_valid():
            product = SupplierProduct(
                    fruit=form.cleaned_data['fruit'],
                    supplier=form.cleaned_data['supplier'],
                    supply_price=form.cleaned_data['supply_price'],
                    last_supply_date=form.cleaned_data['last_supply_date'],
                    quantity_supplied=form.cleaned_data['quantity_supplied'],
                )
            if 'supplier_product_image' in  request.FILES:
                product.supplier_product_image=form.cleaned_data['supplier_product_image'],
            product.save()
            return redirect(reverse("fruit_view"))
            
    return render(request,'shop/create_supplier_product.html',{'form':form})