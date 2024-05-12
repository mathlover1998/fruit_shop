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
    categories_with_subcategories = Category.objects.filter(sub_categories__isnull=False).distinct()
    data = {}

    for category in categories_with_subcategories:
        subcategories = category.sub_categories.all()
        subcategory_data = []

        for subcategory in subcategories:
            products = Product.objects.filter(
                categories__category_name=subcategory.category_name, is_active=True
            ).annotate(category_count=Count("categories"))
            subcategory_count = len(products)
            subcategory_data.append({
                "name": subcategory.category_name,
                "count": subcategory_count
            })

        category_products = Product.objects.filter(
            categories__category_name=category.category_name, is_active=True
        ).annotate(category_count=Count("categories"))
        category_count = len(category_products)

        # Store the original category name in the data dictionary
        category_name = category.category_name.replace(' ', '_').lower()
        data[category_name] = {
            "original_name": category.category_name,
            "count": category_count,
            "subcategories": subcategory_data
        }

    return {"category_context": data}


def get_recently_viewed_products(request):
    products = request.session.get("recently_viewed", {})
    recently_viewed = []
    if products:
        for key, value in products.items():
            try:
                product = get_object_or_404(Product, pk=value)
                recently_viewed.append({"product": product})
            except Product.DoesNotExist:  
                del products[key]
                request.session["recently_viewed"] = products
    return {"recently_viewed_products": recently_viewed}


def get_latest_discounts(request):
    largest_discount_list = Discount.objects.order_by("-valid_to")[:5]
    if not largest_discount_list:
        return {"discount_list": []}
    return {"discount_list": largest_discount_list}




def get_website_information(request):
    try:
        website_info = WebsiteInfo.objects.get(pk=1)  # Try to get the WebsiteInfo record with pk=1
    except WebsiteInfo.DoesNotExist:
        website_info = None
    
    data = {
        'global_instagram_images': [],
        'global_slide_images': [],
        'global_category_images': [],
        'global_about_images': [],
        'global_website_address': None,
        'global_website_email': None,
        'global_website_phone': None,
    }

    if website_info:
        instagram_images = website_info.images.filter(image_type='instagram').order_by('-id')[:10]
        slide_images = website_info.images.filter(image_type='slide').order_by('-id')[:5]
        category_images = website_info.images.filter(image_type='category').order_by('-id')[:3]
        about_images = website_info.images.filter(image_type='about').order_by('-id')[:1]

        data['global_instagram_images'] = [image.image for image in instagram_images]
        data['global_slide_images'] = [image.image for image in slide_images]
        data['global_category_images'] = [image.image for image in category_images]
        data['global_about_images'] = [image.image for image in about_images]

        if website_info.address:
            data['global_website_address'] = website_info.address
        if website_info.email:
            data['global_website_email'] = website_info.email
        if website_info.phone:
            data['global_website_phone'] = website_info.phone
    
    return {'global_information': data}

def get_featured_products_context(request):
    try:
        products = Product.objects.filter(is_featured=True)
        print("Number of featured products:", len(products))
    except Product.DoesNotExist:
        products = []
        
    return {"featured_products":products}