from django.shortcuts import render, HttpResponse, redirect
from fruit_shop_app.models import Product, ProductImage, Order, OrderItem, Address
from django.urls import reverse
from fruit_shop.utils import position_required,replace_string
from .forms import CreateProductForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.db import transaction
from PIL import Image, ImageOps
import os
from django.conf import settings
from uuid import uuid4
from django.db.models import Count
from datetime import timedelta

# Create your views here.


def product_view(request):
    product_list = Product.objects.filter(is_active=True)
    return render(request, "shop/shop.html", {"products": product_list})

def category_filtered_view(request,category):
    product_list = Product.objects.filter(categories__category_name=category,is_active=True)
    return render (request, "shop/shop.html",{"products": product_list})


@login_required
@position_required("inventory_manager", "store_manager")
def create_product(request):
    form = CreateProductForm()
    if request.method == "POST":
        form = CreateProductForm(request.POST, request.FILES)
        if form.is_valid():
            product_name = form.cleaned_data["product_name"]

            product = Product(
                supplier=form.cleaned_data["supplier"],
                product_name=product_name,
                price=form.cleaned_data["price"],
                stock_quantity=form.cleaned_data["stock_quantity"],
                unit = form.cleaned_data["unit"],
                origin_country=form.cleaned_data["origin_country"],
                information=form.cleaned_data["information"],
                create_date=form.cleaned_data["create_date"],
                expiry_date=form.cleaned_data["expiry_date"],
                inventory_manager=request.user.employee,
            )
            product.save()
            category_ids = form.cleaned_data["category"]
            product.categories.set(category_ids)
            product_images = request.FILES.getlist(
                "product_images"
            )  # Get list of uploaded images
            for img in product_images:
                image = Image.open(img)

                # Get dimensions and calculate center coordinates
                width, height = image.size
                center_x = width // 2
                center_y = height // 2

                # Determine the desired size for the centered crop
                desired_width = 255
                desired_height = 241
                half_width = desired_width // 2
                half_height = desired_height // 2

                # Calculate the cropping box coordinates
                left = center_x - half_width
                top = center_y - half_height
                right = center_x + half_width
                bottom = center_y + half_height

                # Crop the image to the center
                cropped_image = image.crop((left, top, right, bottom))

                # Save the cropped image
                cropped_image_path = os.path.join(
                    settings.MEDIA_ROOT, "images/product_images/", f"{uuid4().hex}.jpg"
                )
                cropped_image.save(cropped_image_path)

                ProductImage.objects.create(
                    product=product, image=cropped_image_path
                ).save()

            return redirect(reverse("product_view"))

    return render(request, "shop/create_product.html", {"form": form})


def product_detail(request, product_id):
    product_id_ = str(product_id)
    recently_viewed = request.session.get('recently_viewed', {})
    product = get_object_or_404(Product, pk=product_id)
    if str(product.id) not in recently_viewed:
        recently_viewed[product_id_] = product_id

    request.session['recently_viewed'] = recently_viewed
    request.session.set_expiry(timedelta(days=7))
    return render(request, "shop/product_detail.html", {"product": product})


def add_to_cart(request, product_id, quantity=1):
    product_id_ = str(product_id)
    cart = request.session.get("cart", {})
    product = get_object_or_404(Product, pk=product_id)
    if str(product.id) in cart:
        cart[product_id_]["quantity"] += quantity
    else:
        cart[product_id_] = {"product_id": product_id_, "quantity": quantity}
    request.session["cart"] = cart
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def cart_view(request):
    cart = request.session.get("cart", {})
    cart_items = []
    total_price = 0
    # Retrieve product details for items in the cart
    for item_id, item_data in cart.items():
        product = get_object_or_404(Product, pk=item_id)
        quantity = item_data["quantity"]
        item_total_price = product.price * quantity
        total_price += item_total_price
        cart_items.append(
            {"product": product, "quantity": quantity, "total_price": item_total_price}
        )
    context = {"cart_items": cart_items, "total_price": total_price}
    return render(request, "shop/cart.html", context)


@login_required
def add_to_wishlist(request, product_id):
    product_id_ = str(product_id)
    wishlist = request.session.get("wishlist", {})
    if product_id_ not in wishlist:
        # Use dynamic keys for each product instead of 'product_id'
        wishlist[product_id_] = product_id_
        
    request.session["wishlist"] = wishlist
    request.session.set_expiry(timedelta(days=30))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

@login_required
def wishlist_view(request):
    wishlist = request.session.get("wishlist", {})
    wishlist_items = []
    if not wishlist:
        return 'NOob'
    for key, value in wishlist.items():
        
        product = get_object_or_404(Product, pk=value)
        
        wishlist_items.append(
            {"product": product}
        )
    return render(request,'shop/wishlist.html',{'wishlist_items':wishlist_items})


@login_required
def checkout(request):
    cart = request.session.get("cart", {})
    addresses = Address.objects.filter(customer=request.user.customer).all()

    for address in addresses:
        address_dict = vars(address)
        for key, value in address_dict.items():
            print(f"{key}: {value}")
    order = Order.objects.create(
        customer=request.user.customer,
        total_amount=0,
        payment_status="pending",
    )
    order.save()

    return HttpResponse("Noob")
