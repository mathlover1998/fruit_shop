from fruit_shop_app.models import Product

def cart_item_count(request):
  cart = request.session.get('cart', {})
  product_ids = list(cart.keys())
  products = Product.objects.filter(pk__in=product_ids).prefetch_related('images')

  total_items = sum(item['quantity'] for item in cart.values())
  cart_items = cart

  for item in products:
      if item.images.exists():
          cart_items[str(item.pk)]['image'] = item.images.first().url
      cart_items[str(item.pk)]['name'] = item.product_name
      cart_items[str(item.pk)]['price'] = item.price

  return {'cart_item_count': total_items, 'cart_items': cart_items}