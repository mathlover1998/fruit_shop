from typing import Any
from django.core.exceptions import PermissionDenied
from django.shortcuts import render,redirect
from django.urls import resolve,reverse
from django.http import HttpResponseForbidden,Http404

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
            resolve(request.path_info)
        except Http404:
            return redirect(reverse('error_response',kwargs={'code':404}))
        response = self.get_response(request)
        return response