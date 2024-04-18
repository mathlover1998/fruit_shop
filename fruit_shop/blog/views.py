from django.shortcuts import render
from .models import Blog
from django.http import HttpResponse
# Create your views here.

def blog_list_view(request):
    return HttpResponse('Noob')