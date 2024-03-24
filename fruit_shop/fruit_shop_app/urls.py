from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('',views.index,name='index'),
    path('about/',views.about,name='about_us'),
    path('contact/',views.contact,name='contact_us'),
    path('test/',views.test,name='test'),
    path('save_data/', views.save_data, name='save_data'),
    path('frontend/', TemplateView.as_view(template_name='bin/ajax-test.html'), name='frontend'),
]