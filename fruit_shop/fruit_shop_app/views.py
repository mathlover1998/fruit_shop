from django.shortcuts import render, redirect
from fruit_shop.utils import send_code_via_phone, generate_verification_code
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from fruit_shop_app.models import Supplier


# Create your views here.
def index(request):
    return render(request, "pages/index.html")


def about(request):
    return render(request, "pages/about.html")


def contact(request):
    return render(request, "pages/contact_us.html")


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


def test(request):
    if (
        request.method == "POST"
        and request.headers.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"
    ):
        input_value = request.POST.get("inputField")
        print(input_value)
        return JsonResponse({"result": input_value})
    return render(request, "bin/ajax-test.html")


def save_data(request):
    if request.method == "POST" and request.is_ajax():
        # Assuming your data is sent as JSON
        data = request.POST.get("your_data_key")

        # Save data to the database
        print(data)

        return JsonResponse({"message": "Data saved successfully"})
    else:
        return JsonResponse({"error": "Invalid request"})
