from django.shortcuts import render, redirect
from fruit_shop.utils import send_code_via_phone, generate_verification_code
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from fruit_shop_app.models import Supplier,Product
from django.contrib.sessions.models import Session
from django.utils import timezone


# Create your views here.
def index(request):
    return render(request, "pages/index.html")


def about_us(request):
    return render(request, "pages/about.html")


def contact(request):
    return render(request, "pages/contact_us.html")

def location(request):
    return render(request,'pages/location.html')


def supplier_register(request):
    if request.method == "POST":
        supplier_name = request.POST.get("supplier_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        new_supplier = Supplier.objects.create(
            supplier_name=supplier_name, email=email, phone=phone
        )
        new_supplier.save()
        return redirect(reverse("confirmation_page"))
    return render(request, "account/supplier_register.html")


def confirmation_page(request):
    return render(request, "notification/wait_for_confirmation.html")


def clear_session(request):
    expired_sessions = Session.objects.filter(expire_date__lt=timezone.now())
    expired_sessions.delete()
    Session.objects.all().delete()
    return HttpResponse("Sessions cleared successfully")
