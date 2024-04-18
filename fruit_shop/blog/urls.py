from django.urls import path
from . import views
urlpatterns = [
    path('',views.get_all_blogs,name='get_all_blogs')
]