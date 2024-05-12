from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('',views.index,name='index'),
    path('about-us/',views.view_about_us ,name='view_about_us '),
    path('contact-us/',views.handle_contact_us,name='handle_contact_us'),
    path('location/',views.view_location,name='view_location'),
    path('confirmation/', views.view_confirmation_page, name='view_confirmation_page'),
    path('error/<int:code>/',views.error_response,name='error_response'),
    path('brand-register/',views.brand_register,name='brand_register'),
    path('receive-newsletter/',views.register_newsletter,name='register_newsletter'),
    path('clear/',views.clear_session,name='clear_session'),
]