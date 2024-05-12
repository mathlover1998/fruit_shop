from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.sessions.models import Session
from django.utils import timezone
from fruit_shop.utils import send_specific_email
from django.views.decorators.csrf import csrf_exempt
from fruit_shop.utils import send_specific_email

# Create your views here.
def index(request):
    return render(request, "pages/index.html")


def view_about_us (request):
    return render(request, "pages/about.html")


def handle_contact_us(request):
    # if request.method=='POST':
    #     name = request.POST.get('name')
    #     email = request.POST.get('email')
    #     subject = request.POST.get('subject')
    #     content = request.POST.get('content')
    #     send_specific_email(request=request,email_list=[email],choice=)
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
    return HttpResponse("Sessions cleared successfully")

@csrf_exempt
def register_newsletter(request):
    if request.method=='POST':
        email= request.POST.get('email')
        send_specific_email(request=request,choice=4,email_list=[email])
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))