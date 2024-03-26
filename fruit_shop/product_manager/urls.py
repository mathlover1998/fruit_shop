from django.urls import path
from . import views

urlpatterns = [
    path('',views.product_view,name='product_view'),
    path('fruits/',views.create_fruit,name='create_fruit'),
    path('supplier/register/',views.supplier_register,name='supplier_register'),
    path('confirmation/', views.confirmation_page, name='confirmation_page')
    
]