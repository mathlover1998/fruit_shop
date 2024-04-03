from fruit_shop_app.models import Product, Category
from django.shortcuts import get_object_or_404


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
    products = Product.objects.all()[:10]
    exclusive = Product.objects.filter(categories__category_name="Exclusive")
    plant_based = Product.objects.filter(
        categories__category_name="Plant-based Produce"
    )
    sea_food = Product.objects.filter(categories__category_name="Seafood")
    meat = Product.objects.filter(categories__category_name="Meat")
    dairy_products = Product.objects.filter(categories__category_name="Dairy Product")
    processed_foods = Product.objects.filter(categories__category_name="Processed food")
    essential_ingredients = Product.objects.filter(
        categories__category_name="Essential Ingredient"
    )
    return {"global_products":products,"global_exclusive":exclusive,"global_plant_based":plant_based}
