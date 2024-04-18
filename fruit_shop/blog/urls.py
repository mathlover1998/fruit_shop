from django.urls import path
from . import views
urlpatterns = [
    path('',views.blog_list_view,name='blog_list_view')
]