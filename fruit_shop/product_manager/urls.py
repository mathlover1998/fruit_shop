from django.urls import path
from . import views

urlpatterns = [
    path('',views.product_view,name='product_view'),
    path('supplier/register/',views.supplier_register,name='supplier_register'),
    path('confirmation/', views.confirmation_page, name='confirmation_page'),
    path('fruit/create/',views.create_fruit,name='create_fruit'),
    path('fruits/',views.fruit_view, name='fruit_view'),
    path('create/',views.create_product,name='create_product')
]