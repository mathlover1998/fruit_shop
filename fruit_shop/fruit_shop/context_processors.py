from fruit_shop_app.models import Product, Category, Discount,WebsiteInfo
from django.shortcuts import get_object_or_404
from django.db.models import Count


def get_global_cart_data(request):
    cart = request.session.get("cart", {})
    cart_items = []
    if not cart:
        return {
            "global_cart_items": [],
            "global_cart_items_count": 0,
            "global_total_price": 0,
        }
    for key, value in cart.items():
        product = get_object_or_404(Product, pk=key)
        quantity = value["quantity"]
        item_total_price = product.price * quantity

        cart_items.append(
            {"product": product, "quantity": quantity, "total_price": item_total_price}
        )
        total_price = 0
        for item in cart_items:
            total_price += item["total_price"]

    return {
        "global_cart_items": cart_items,
        "global_cart_items_count": len(cart),
        "global_total_price": total_price,
    }


def get_separated_category_product(request):
    global_categories = {}
    categories = Category.objects.filter(parent_category__isnull=True).values_list(
        "category_name", flat=True
    )
    for category in categories:
        products = Product.objects.filter(
            categories__category_name=category, is_active=True
        ).annotate(category_count=Count("categories"))
        global_categories[f"{category.replace(' ', '_').lower()}"] = products.filter(
            category_count=1
        )[:2]
    return {"separated_category_products": global_categories}


def get_category_name_context(request):
    categories = Category.objects.all().values_list("category_name", flat=True)
    data = {}
    for category in categories:
        products = Product.objects.filter(
            categories__category_name=category, is_active=True
        ).annotate(category_count=Count("categories"))
        data[f"{category.replace(' ', '_').lower()}_count"] = len(products)
    return {"category_context": data}


def get_recently_viewed_products(request):
    products = request.session.get("recently_viewed", {})
    recently_view = []
    if not products:
        return {"cart_items": [], "cart_items_count": 0, "total_price": 0}
    for key, value in products.items():

        product = get_object_or_404(Product, pk=value)

        recently_view.append({"product": product})

    return {"recently_viewed_products": recently_view}


def get_latest_discounts(request):
    largest_discount_list = Discount.objects.order_by("-valid_to")[:5]
    if not largest_discount_list:
        return {"discount_list": []}
    return {"discount_list": largest_discount_list}


def get_website_information(request):
    website_info = get_object_or_404(WebsiteInfo,pk=1)
    instagram_images = website_info.images.filter(image_type='instagram').order_by('-id')[:10] #take at least 5 slide images
    slide_images = website_info.images.filter(image_type='slide').order_by('-id')[:5] #take at least 5 slide images
    category_images = website_info.images.filter(image_type='category').order_by('-id')[:3] #only take 3 latest category images
    about_images = website_info.images.filter(image_type='about').order_by('-id')[:1] #only take 1 about image
    data = {
        'global_instagram_images': [image.image for image in instagram_images],
        'global_slide_images': [image.image for image in slide_images],
        'global_category_images': [image.image for image in category_images],
        'global_about_images': [image.image for image in about_images],
    }

    if website_info.address:
        data['global_website_address'] = website_info.address
    if website_info.email:
        data['global_website_email'] = website_info.email
    if website_info.phone:
        data['global_website_phone'] = website_info.phone
    return {'global_information':data}