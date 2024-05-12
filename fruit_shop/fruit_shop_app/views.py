from django.shortcuts import render, redirect
from fruit_shop.utils import send_code_via_phone, generate_verification_code
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from fruit_shop_app.models import Brand,Product
from django.contrib.sessions.models import Session
from django.utils import timezone
from fruit_shop.utils import send_specific_email
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    return render(request, "pages/index.html")


def view_about_us (request):
    return render(request, "pages/about.html")


def handle_contact_us(request):
    return render(request, "pages/contact_us.html")

def view_location(request):
    return render(request,'pages/location.html')


def brand_register(request):
    if request.method == "POST":
        brand_name = request.POST.get("brand_name")
        contact_person = request.POST.get("contact_person")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        new_brand = Brand.objects.create(
            brand_name=brand_name, contact_person=contact_person, email=email, phone=phone
        )
        new_brand.save()
        return redirect(reverse("view_confirmation_page"))
    return render(request, "account/brand_register.html")


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