from django.urls import path
from . import views

urlpatterns = [
    path("", views.product_view, name="product_view"),
    path("create/", views.create_product, name="create_product"),
    path("<int:product_id>",views.product_detail,name="product_detail"),
    path('cart',views.cart_view,name='cart_view'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    
    
]
