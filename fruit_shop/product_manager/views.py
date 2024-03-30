from django.shortcuts import render, HttpResponse, redirect
from fruit_shop_app.models import Product, Supplier,ProductImage
from django.urls import reverse
from fruit_shop.utils import position_required
from .forms import CreateProductForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Create your views here.


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
            product.save()
            product_images = request.FILES.getlist('product_images')  # Get list of uploaded images
            for img in product_images:
                ProductImage.objects.create(product=product,image=img).save()
            return redirect(reverse("product_view"))

    return render(request, "shop/create_product.html", {"form": form})

def product_detail(request,product_id):
    product = Product.objects.filter(pk=product_id).first()
    return render(request,'shop/product_detail.html',{'product':product})