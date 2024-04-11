from django.urls import path
from . import views

urlpatterns = [
    path("", views.product_view, name="product_view"),
    path("create/", views.create_product, name="create_product"),
    path("<int:product_id>",views.product_detail,name="product_detail"),
    path('cart',views.cart_view,name='cart_view'),
    path('add-to-cart/<int:product_id>/<int:quantity>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/',views.checkout,name='checkout'),
    path("<str:category>/",views.category_filtered_view,name='category_filtered_view'),
    path('add-to-wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist',views.wishlist_view,name='wishlist_view'),
    path('remove-wishlist/<int:product_id>/',views.remove_from_wishlist,name='remove_from_wishlist')

]
