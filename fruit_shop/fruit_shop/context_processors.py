from fruit_shop_app.models import Product, Category
from django.shortcuts import get_object_or_404
from django.db.models import Count


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
    exclusive = (
        Product.objects.filter(categories__category_name="Exclusive")
        .annotate(category_count=Count("categories"))
        .filter(category_count=1)[:2]
    )
    plant_based = (
        Product.objects.filter(categories__category_name="Plant-based Produce")
        .annotate(category_count=Count("categories"))
        .filter(category_count=1)[:2]
    )
    sea_food = (
        Product.objects.filter(categories__category_name="Seafood")
        .annotate(category_count=Count("categories"))
        .filter(category_count=1)[:2]
    )
    meat = (
        Product.objects.filter(categories__category_name="Meat")
        .annotate(category_count=Count("categories"))
        .filter(category_count=1)[:2]
    )
    dairy_products = (
        Product.objects.filter(categories__category_name="Dairy Product")
        .annotate(category_count=Count("categories"))
        .filter(category_count=1)[:2]
    )
    processed_foods = (
        Product.objects.filter(categories__category_name="Processed Food")
        .annotate(category_count=Count("categories"))
        .filter(category_count=1)[:2]
    )
    essential_ingredients = (
        Product.objects.filter(categories__category_name="Essential Ingredient")
        .annotate(category_count=Count("categories"))
        .filter(category_count=1)[:2]
    )
    return {
        "global_exclusive": exclusive,
        "global_plant_based": plant_based,
        "global_sea_food": sea_food,
        "global_meat": meat,
        "global_dairy_products": dairy_products,
        "global_processed_foods": processed_foods,
        "global_essential_ingredients": essential_ingredients,
    }
