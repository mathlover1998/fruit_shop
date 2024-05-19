from typing import Any
from django.core.exceptions import PermissionDenied
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import resolve,reverse
from django.http import HttpResponseForbidden,Http404
from fruit_shop_app.models import Product
from django.utils.deprecation import MiddlewareMixin


class CustomPermissionDeniedMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response
    
    def __call__(self,request):
        response = self.get_response(request)
        return response
    
    def process_exception(self, request, exception):
        if isinstance(exception, PermissionDenied):

            return redirect(reverse("error_response", kwargs={"code": 403}))
            
        
class CheckURLMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Http404:
            return redirect(reverse('error_response',kwargs={'code':404}))
        
class CheckProductExistMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if 'sku' in view_kwargs:
            sku = view_kwargs['sku']
            try:
                # Check if the product with the given SKU exists
                get_object_or_404(Product, sku=sku)
            except Http404:
                # If the product does not exist, raise a 404 error
                return redirect(reverse("error_response", kwargs={"code": 404}))