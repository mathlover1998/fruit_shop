from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse,FileResponse
from django.urls import reverse
from django.contrib.sessions.models import Session
from django.utils import timezone
from common.utils import send_specific_email,modify_excel_file
from django.views.decorators.csrf import csrf_exempt
from common import error_messages
from fruit_shop_app.models import ContactUsMessage,Product,Discount,Order
import json
from django.conf import settings
from urllib.parse import urljoin

# Create your views here.
def index(request):
    return render(request, "pages/index.html")


def view_about_us (request):
    return render(request, "pages/about.html")


def handle_contact_us(request):
    if request.method=='POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        content = request.POST.get('content')
        required_fields = [name,email,subject,content]
        if all(required_fields):
            ContactUsMessage.objects.create(name=name,email=email,subject=subject,content=content).save()
            send_specific_email(request=request,email_list=[email],choice=4)
            return JsonResponse({'success':True,'success_message':error_messages.GENERAL_NOTIFICATION})
        return JsonResponse({'success': False, 'error_message': error_messages.MISSING_FIELDS})
    return render(request, "pages/contact_us.html")
    

def view_location(request):
    return render(request,'pages/location.html')



def view_confirmation_page(request):
    return render(request, "notification/wait_for_confirmation.html")


def error_response(request,code):
    return render(request,'errors/error_response.html',{'status_code':code})


def clear_session(request):
    expired_sessions = Session.objects.filter(expire_date__lt=timezone.now())
    expired_sessions.delete()
    Session.objects.all().delete()
    response = HttpResponse("Cookie Cleared")
    response.delete_cookie('cookie_name')
    return response

@csrf_exempt
def register_newsletter(request):
    if request.method=='POST':
        email= request.POST.get('email')
        send_specific_email(request=request,choice=4,email_list=[email])
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
    

def search_result(request):
    query = request.GET.get('q')
    
    if query:
        products = Product.objects.filter(product_name__icontains=query)
    else:
        products = Product.objects.none()
    
    return render(request, 'shop/search-results.html', {'products': products, 'query': query})

def download_template(request):
    file_path = modify_excel_file()
    response = redirect(urljoin('https://'+settings.AWS_S3_CUSTOM_DOMAIN +'/',file_path))
    response['Content-Disposition'] = 'attachment; filename="products.xlsx"'
    return response
    # return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='modified_template.xlsx')



