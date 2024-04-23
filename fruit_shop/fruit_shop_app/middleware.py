from typing import Any
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.http import HttpResponseForbidden

class CustomPermissionDeniedMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response
    
    def __call__(self,request):
        response = self.get_response(request)
        return response
    
    def process_exception(self, request, exception):
        if isinstance(exception, PermissionDenied):
            return render(request,'errors/error_response.html',{'status_code':int(403)})