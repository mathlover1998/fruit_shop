from fruit_shop_app.models import Product, Category
from django.shortcuts import get_object_or_404
from django.db.models import Count

categories = [
        "Exclusive",
        "Plant-based Produce",
        "Seafood",
        "Meat",
        "Dairy Product",
        "Processed Food",
        "Essential Ingredient"
    ]

def cart_item_count(request):
    cart = request.session.get("cart", {})
    cart_items = []
    if not cart:
        return {"cart_items": [], "cart_items_count": 0, "total_price": 0}
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


def product_filtered(request):
    global_categories = {}
    for category in categories:
        products = Product.objects.filter(categories__category_name=category).annotate(
            category_count=Count("categories")
        )
        global_categories[f"{category.replace(' ', '_').lower()}"] = products.filter(category_count=1)[:2]
    return {'global_category':global_categories}

def category_count(request):
    data = {}
    for category in categories:
        products = Product.objects.filter(categories__category_name=category).annotate(
            category_count=Count("categories")
        )
        data[f"{category.replace(' ', '_').lower()}_count"] = len(products)
    return {'category_count': data}
