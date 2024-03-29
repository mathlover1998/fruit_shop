from django.shortcuts import render, HttpResponse, redirect
from fruit_shop_app.models import Product, Supplier
from django.urls import reverse
from fruit_shop.utils import position_required
from .forms import CreateProductForm
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
    product_list = Product.objects.all()
    return render(request, "shop/shop.html", {"products": product_list})


@login_required
@position_required("inventory_manager", "store_manager")
def create_product(request):
    form = CreateProductForm()
    if request.method == "POST":
        form = CreateProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = Product(
                supplier=form.cleaned_data["supplier"],
                product_name=form.cleaned_data["product_name"],
                category=form.cleaned_data["category"],
                price=form.cleaned_data["price"],
                stock_quantity=form.cleaned_data["stock_quantity"],
                origin_country=form.cleaned_data["origin_country"],
                information=form.cleaned_data["information"],
                create_date=form.cleaned_data["create_date"],
                expiry_date=form.cleaned_data["expiry_date"],
                inventory_manager=request.user.employee,
            )
            if "product_image" in request.FILES:
                product.product_image = (form.cleaned_data["product_image"],)
            product.save()
            return redirect(reverse("product_view"))

    return render(request, "shop/create_product.html", {"form": form})
