from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_all_products, name="get_all_products"),
    path('my-products/',views.get_your_products,name='get_your_products'),
    path("create/", views.create_product, name="create_product"),
    path("<str:sku>/",views.get_product,name="get_product"),#
    path("filter/<str:category>/",views.category_filtered_view,name='category_filtered_view'),#
    path('wishlist',views.get_wishlist,name='get_wishlist'),
    path('wishlist/add/<int:product_id>/', views.update_wishlist_item, name='update_wishlist_item'),
    path('wishlist/delete/<int:product_id>/',views.delete_wishlist_item,name='delete_wishlist_item'),
    path('cart/',views.get_cart,name='get_cart'),
    path('cart/add/<int:product_id>/<int:quantity>/', views.update_cart_item, name='update_cart_item'),
    path('cart/delete/<int:product_id>/',views.delete_cart_item,name='delete_cart_item'),
    path('checkout/',views.checkout,name='checkout'),
    path('<str:sku>/update/',views.update_product, name="update_product"),

]
