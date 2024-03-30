from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('',views.index,name='index'),
    path('about-us/',views.about_us,name='about_us'),
    path('contact/',views.contact,name='contact_us'),
    path('location/',views.location,name='location'),
    path('supplier/register/',views.supplier_register,name='supplier_register'),
    path('confirmation/', views.confirmation_page, name='confirmation_page'),
]