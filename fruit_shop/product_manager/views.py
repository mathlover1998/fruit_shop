from django.shortcuts import render, HttpResponse, redirect
from fruit_shop_app.models import Product,ProductImage,Order,OrderItem,Address,Transaction,Comment,Brand,Category
from django.contrib import messages
from django.urls import reverse
from common.utils import convert_to_csv,handle_uploaded_file
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.db import transaction
from PIL import Image
import os, json
from django.conf import settings
from uuid import uuid4
from datetime import timedelta
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from common import error_messages
import pandas as pd


# Create your views here.
def calculate_total_price(cart):
    total_price = 0

    for product_id, item_data in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        quantity = item_data["quantity"]
        total_price += product.price * quantity

    return total_price


def get_all_products(request):
    product_list = Product.objects.filter(is_active=True)
    return render(request, "shop/shop.html", {"products": product_list})


def category_filtered_view(request, category):
    product_list = Product.objects.filter(
        categories__category_name=category, is_active=True
    )
    return render(request, "shop/shop.html", {"products": product_list})

def get_your_products(request):
    current_employee = request.user.employee
    product_lists = Product.objects.filter(inventory_manager=current_employee)
    return render(request,'shop/my_products.html',{'products':product_lists})

def upload_file(request):
    if request.method == 'POST':
        file_path = handle_uploaded_file(request.FILES['file'])
        csv_file_path = convert_to_csv(file_path)
        df = pd.read_csv(csv_file_path)
        if df.empty:
            return JsonResponse({'error': 'The uploaded file is empty or invalid'}, status=400)
        for index, row in df.iterrows():
            categories =Category.objects.filter(category_name=row.iloc[9])
            brand = Brand.objects.filter(brand_name=row.iloc[8]).first()

            common_args = {
            "brand": brand,
            "product_name": row.iloc[0],
            "price": row.iloc[1],
            "stock_quantity": row.iloc[4],
            "origin_country": row.iloc[5],
            "information": row.iloc[6],
            "unit": row.iloc[3]
            }

            if row.iloc[7]:
                common_args["sku"] = row.iloc[7]

            product = Product.objects.create(**common_args)
            product.save()
            all_categories = set(categories)
            for category in categories:
                current_category = category
                while current_category.parent_category:
                    all_categories.add(current_category.parent_category)
                    current_category = current_category.parent_category
            product.categories.set(all_categories)
            ProductImage.objects.create(product=product, image=row.iloc[2]).save()
        # with open(csv_file_path, 'rb') as f:
        #     response = HttpResponse(f.read(), content_type='text/csv')
        #     response['Content-Disposition'] = f'attachment; filename={os.path.basename(csv_file_path)}'
        #     return response
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
            
    return render(request, 'shop/manage_product.html')


@permission_required('fruit_shop_app.add_product',raise_exception=True)
def create_product(request):
    form = ProductForm()
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product_name = form.cleaned_data["product_name"]

            product = Product(
                brand=form.cleaned_data["brand"],
                product_name=product_name,
                price=form.cleaned_data["price"],
                stock_quantity=form.cleaned_data["stock_quantity"],
                unit=form.cleaned_data["unit"],
                origin_country=form.cleaned_data["origin_country"],
                information=form.cleaned_data["information"],
                inventory_manager=request.user.employee,
            )
            product.save()
            #if category has parent_category, also add to parent_category
            categories = form.cleaned_data["category"]
            all_categories = set(categories)
            for category in categories:
                current_category = category
                while current_category.parent_category:
                    all_categories.add(current_category.parent_category)
                    current_category = current_category.parent_category
            product.categories.set(all_categories)
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

            return JsonResponse({'success': True})

    return render(request, "shop/manage_product.html", {"form": form,'is_update':False})

@permission_required('fruit_shop_app.change_product', raise_exception=True)
def update_product(request,sku):
    product = get_object_or_404(Product, sku=sku)
    # Get current product images
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product.product_name = form.cleaned_data["product_name"]
            product.brand=form.cleaned_data["brand"]
            product.price=form.cleaned_data["price"]
            product.stock_quantity=form.cleaned_data["stock_quantity"]
            product.unit=form.cleaned_data["unit"]
            product.origin_country=form.cleaned_data["origin_country"]
            product.information=form.cleaned_data["information"]

            category_ids = form.cleaned_data["category"]
            product.categories.set(category_ids)
            #if category has parent_category, also add to parent_category
            categories = form.cleaned_data["category"]
            all_categories = set(categories)
            for category in categories:
                current_category = category
                while current_category.parent_category:
                    all_categories.add(current_category.parent_category)
                    current_category = current_category.parent_category
            product.categories.set(all_categories)
            product.save()
            #delete all current images
            ProductImage.objects.filter(product=product).delete()
            # Handle new product image uploads
            product_images = request.FILES.getlist("product_images")
            for img in product_images:
                image = Image.open(img)
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
                # Perform image processing (similar to create_product)

                try:
                    # Save the cropped image
                    cropped_image_path = os.path.join(
                        settings.MEDIA_ROOT,
                        "images/product_images/",
                        f"{uuid4().hex}.jpg",
                    )
                    cropped_image.save(cropped_image_path)

                    ProductImage.objects.create(
                        product=product, image=cropped_image_path
                    ).save()
                except (ValidationError, OSError) as e:
                    return JsonResponse({'success': False, 'error_message': error_messages.INVALID_IMAGE})

            return JsonResponse({'success': True})

    else:
        # Populate form with product data
        form = ProductForm(initial=model_to_dict(product))

    return render(
        request,
        "shop/update_product.html",
        {"form": form, "product": product,'is_update':True},
    )



def get_product(request,sku):
    product = get_object_or_404(Product, sku=sku)
    product_id = product.id
    comments = Comment.objects.filter(product=product)
    recently_viewed = request.session.get("recently_viewed", {})
    if str(product.id) not in recently_viewed:
        recently_viewed[str(product_id)] = product_id

    request.session["recently_viewed"] = recently_viewed
    request.session.set_expiry(timedelta(days=7))

    return render(request, "shop/product.html", {"product": product,'comments':comments})


def update_cart_item(request, product_id, quantity=1):
    product_id_ = str(product_id)
    cart = request.session.get("cart", {})
    product = get_object_or_404(Product, pk=product_id)
    if str(product.id) in cart:
        cart[product_id_]["quantity"] += quantity
    else:
        cart[product_id_] = {"product_id": product_id_, "quantity": quantity}
    request.session["cart"] = cart
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


def get_cart(request):
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
def delete_cart_item(request, product_id):
    cart = request.session.get("cart", {})

    # Check if the product_id exists in the wishlist
    if str(product_id) in cart:
        # Remove the product_id from the wishlist
        del cart[str(product_id)]

        # Update the session data
        request.session["cart"] = cart
        request.session.modified = True  # Make sure to mark the session as modified

    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


@login_required
def update_wishlist_item(request, product_id):
    product_id_ = str(product_id)
    wishlist = json.loads(request.COOKIES.get("wishlist", "{}"))
    if product_id_ not in wishlist:
        # Use dynamic keys for each product instead of 'product_id'
        wishlist[product_id_] = product_id_

    response = HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
    response.set_cookie("wishlist", json.dumps(wishlist), max_age=timedelta(days=30))
    return response


@login_required
def get_wishlist(request):
    wishlist = json.loads(request.COOKIES.get("wishlist", "{}"))
    wishlist_items = []

    for key, value in wishlist.items():
        product = get_object_or_404(Product, pk=value)
        wishlist_items.append({"product": product})

    return render(request, "shop/wishlist.html", {"wishlist_items": wishlist_items})


@login_required
def delete_wishlist_item(request, product_id):
    wishlist = json.loads(request.COOKIES.get("wishlist", "{}"))

    if str(product_id) in wishlist:
        del wishlist[str(product_id)]

    response = HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
    response.set_cookie("wishlist", json.dumps(wishlist), max_age=timedelta(days=30))
    return response


@login_required
@transaction.atomic
def checkout(request):
    current_user = request.user
    address_list = Address.objects.filter(user=current_user)
    cart = request.session.get("cart", {})
    cart_items = []
    total_price = 0

    for item_id, item_data in cart.items():
        product = get_object_or_404(Product, pk=item_id)
        quantity = item_data["quantity"]
        item_total_price = product.price * quantity
        total_price += item_total_price
        cart_items.append(
            {
                "product": product,
                "quantity": quantity,
                "total_price": item_total_price,
            }
        )
    if request.method == "POST":
        # Assuming you have a form submission with necessary checkout details
        payment_method = request.POST.get("payment_method")
        address_id = request.POST.get("address")
        address = Address.objects.filter(user=request.user,pk=address)
        print(address.street_address)
        # Check if payment method is cash on delivery
        if payment_method == "cash":

            order = Order.objects.create(
                payment_method = payment_method,
                customer=request.user.customer,
                total_amount=0,
                status="pending",
                shipping_address=Address.objects.filter(pk=request.POST.get("address")),
                
            )
            total_amount = 0
            for item_id, item_data in cart.items():
                product = Product.objects.get(pk=item_id)
                quantity = item_data["quantity"]
                subtotal = product.price * quantity
                total_amount += subtotal

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    subtotal=subtotal,
                )

                product.stock_quantity -= quantity
                product.save()

            order.total_amount = total_amount
            order.save()

            transaction = Transaction.objects.create(
                order=order,
                payment_method=payment_method,
                amount_paid=0,
            )
            transaction.save()
            order.payment_transaction = transaction.pk
            order.save()
            request.session["cart"] = {}

            return redirect(reverse("view_confirmation_page"))
        else:
            return HttpResponse("Payment method not supported yet.")

    return render(
        request,
        "shop/checkout.html",
        {
            "address_list": address_list,
            "cart_items": cart_items,
            "total_price": total_price,
        },
    )


def create_discount(request):
    pass

def apply_discount_view(request):
    products_with_category_discount = Product.objects.filter(categories__discount__is_active=True)
    # You can then use 'products_with_brand_discount' as needed
    for product in products_with_category_discount:
        print(product.product_name)
    return render(request, 'shop/discount_applied.html')

@login_required
def create_comment_on_product(request, sku):
    user = request.user
    product = Product.objects.filter(sku=sku).first()
    if request.method == 'POST':
        comment = Comment.objects.create(
            user=user,
            product=product,
            content=request.POST.get('content')
        )
        comment.save()
        return redirect(reverse('get_product', kwargs={'sku': sku}))
    
    return render(request, 'shop/product.html')

    
@login_required
def delete_comment_on_product(request,sku):
    comment_id = request.GET.get('comment_id')
    comment = Comment.objects.filter(id= comment_id)
    comment.delete()
    return redirect(reverse('get_product', kwargs={'sku': sku}))

@login_required
def update_comment_on_product(request, sku):
    comment_id = request.POST.get('comment_id')
    comment = Comment.objects.get(id=comment_id)
    if request.method == 'POST':
        comment.content = request.POST.get('content')
        comment.save()
        return redirect(reverse('get_product', kwargs={'sku': sku}))
    return render(request, 'shop/edit_comment.html', {'comment': comment})

@permission_required('fruit_shop_app.add_brand',raise_exception=True)
def create_brand(request):
    if request.method == "POST":
        brand_name = request.POST.get("brand_name")
        contact_person = request.POST.get("contact_person")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        fields = [brand_name,contact_person,email,phone]
        if all(fields):
            new_brand = Brand.objects.create(
                brand_name=brand_name, contact_person=contact_person, email=email, phone=phone
            )
            new_brand.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'error_message': error_messages.MISSING_FIELDS})
    return render(request, "account/create_brand.html")
