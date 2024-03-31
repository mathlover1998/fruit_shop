from django.shortcuts import render, HttpResponse, redirect
from fruit_shop_app.models import Product, ProductImage, Order, OrderItem,Address
from django.urls import reverse
from fruit_shop.utils import position_required
from .forms import CreateProductForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db import transaction

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
            product_images = request.FILES.getlist(
                "product_images"
            )  # Get list of uploaded images
            for img in product_images:
                ProductImage.objects.create(product=product, image=img).save()
            return redirect(reverse("product_view"))

    return render(request, "shop/create_product.html", {"form": form})


def product_detail(request, product_id):
    product = Product.objects.filter(pk=product_id).first()
    return render(request, "shop/product_detail.html", {"product": product})


def add_to_cart(request, product_id, quantity=1):
    cart = request.session.get("cart", {})
    product = get_object_or_404(Product, pk=product_id)
    if product.id in cart:
        cart[product_id]["quantity"] += quantity
    else:
        cart[product_id] = {"quantity": quantity}
    request.session["cart"] = cart
    print(cart[product_id]["quantity"])
    print(cart)
    return redirect(reverse("product_view"))


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
def checkout(request):
    cart = request.session.get("cart", {})
    addresses = Address.objects.filter(customer = request.user.customer).all()

    for address in addresses:
        address_dict = vars(address)
        for key,value in address_dict.items():
            print(f'{key}: {value}')
    order = Order.objects.create(
        customer = request.user.customer,
        total_amount = 0,
        payment_status = 'pending',
        )
    order.save()
    
    return HttpResponse('Noob')


# def best_seller(request):
#     return render(request,'shop/gallery.html')
