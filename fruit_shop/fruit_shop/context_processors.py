from fruit_shop_app.models import Product
from django.shortcuts import get_object_or_404
from django.templatetags.static import static

def cart_item_count(request):
    cart = request.session.get("cart", {})
    cart_items = []
    if not cart: 
        return {"cart_items": [], 'cart_items_count': 0, 'total_price': 0}
    for key, value in cart.items():
        product = get_object_or_404(Product,pk = key)
        quantity = value["quantity"]
        item_total_price = product.price * quantity
        
        cart_items.append(
            {"product": product, "quantity": quantity, "total_price": item_total_price}
        )
        total_price = 0
        for item in cart_items:
            print(item['total_price'])
            total_price+= item['total_price']
        
    return {"cart_items": cart_items,'cart_items_count':len(cart),'total_price':total_price}
