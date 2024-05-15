import os, asyncio
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from fruit_shop_app.models import User, Customer, Address, Employee
from django.contrib import messages
from django.template.loader import render_to_string
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required, user_passes_test
from common.utils import *
from django.template.defaultfilters import date
from django.utils.html import strip_tags
from django.contrib.sessions.models import Session
from django.views.decorators.csrf import csrf_exempt
from django.http import (
    JsonResponse,
    HttpResponseForbidden,
    HttpResponseRedirect,
    HttpResponseBadRequest,
)
from django.core.serializers import serialize
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.http import require_POST
from datetime import timedelta
from functools import wraps
from django.db import transaction
from common import error_messages

# Create your views here.


def register_customer(request):
    if request.method == "POST":
        username = request.POST.get("username")
        if User.objects.filter(username=username).exists():
            return JsonResponse({'success':False,'error_message':error_messages.USERNAME_IS_TAKEN})
        else:
            password = request.POST.get("password")
            re_password = request.POST.get("re_password")
            if password == re_password:
                request.session["username"] = username
                request.session["password"] = password
                return JsonResponse({'success': True})
            return JsonResponse({'success':False,'error_message':error_messages.PASSWORDS_DO_NOT_MATCH})
    return render(request, "account/register.html")


def collect_customer_registration_email(request):
    if request.method == "POST":
        email = request.POST.get("email")
        username = request.session.get("username")
        password = request.session.get("password")
        if not username:
            return JsonResponse({'success':False,'error_message':error_messages.GENERAL_ERROR})
        if User.objects.filter(email=email).exists():
            return JsonResponse({'success':False,'error_message':error_messages.EMAIL_IS_TAKEN})
        else:
            user = User.objects.create_user(username=username, password=password)
            user.email = email
            user.save()
            Customer.objects.create(user=user).save()
            send_specific_email(request=request, choice=1, email_list=[email])
            login(request, user)
            return JsonResponse({'success':True})
    return render(request, "account/enter_verification_email.html")


def handle_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error_message': error_messages.LOGIN_FAILED})

    return render(request, "account/log_in.html")


@login_required
def handle_logout(request):
    logout(request)
    return redirect(reverse("index"))


@login_required
def view_user_account(request):
    return render(request, "account/account.html")


@login_required
def update_profile(request):
    current_user = request.user
    full_name = current_user.get_full_name()
    email = mask_email(current_user.email)
    phone = validate_mask_phone(current_user.phone)
    dob_formatted = date(current_user.dob, "Y-m-d") if current_user.dob else None
    if request.method == "POST":
        image = request.FILES.get("image")
        full_name = request.POST.get("full_name")
        gender = request.POST.get("gender")
        dob = request.POST.get("dob")

        if not (image or full_name or gender or dob):
            return JsonResponse({'success': False, 'error_message': error_messages.MISSING_FIELDS})

        if image:
            current_user.image = image
        if full_name:
            current_user.first_name, current_user.last_name = full_name.split(
                maxsplit=1
            )

        if gender:
            current_user.gender = gender
        if dob:
            current_user.dob = dob
        current_user.save()
        return JsonResponse({'success': True,'success_message':error_messages.UPDATE_SUCCESSFULLY})
    return render(
        request,
        "account/profile.html",
        {
            "current_user": current_user,
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "dob": dob_formatted,
        },
    )


@login_required
def update_email(request):
    if request.method == "POST":
        current_user = request.user
        email = request.POST.get("email")
        receive_updates = request.POST.get("receive_updates", False)

        if receive_updates:
            send_specific_email(request=request, choice=2, email_list=[email])
            current_user.receive_updates = True
            current_user.save()
        if (
            not email
            or User.objects.exclude(pk=current_user.id).filter(email=email).exists()
        ):
            return JsonResponse({'success': False, 'error_message': error_messages.EMAIL_IS_TAKEN})
        else:
            code = generate_verification_code()
            request.session["email_verification_code"] = code
            # Set session expiry to 10 minutes from now
            request.session.set_expiry(timedelta(minutes=10))
            send_specific_email(
                request=request, choice=3, email_list=[email], code=code
            )
            return JsonResponse({
            'success': True,'redirect_url': reverse('handle_verification_code', kwargs={'email_or_phone': email})
        })    
    return render(request, "account/update_new_email.html")


@login_required
def update_phone(request):
    if request.method == "POST":
        phone_number = request.POST.get("phone")
        # Check if the phone number is valid
        if not is_phone_number(phone_number):
            return JsonResponse({'success': False, 'error_message': error_messages.PHONE_NUMBER_FORMAT_INVALID})
        # Check if the phone number is already taken
        if User.objects.filter(phone=phone_number).exists():
           return JsonResponse({'success': False, 'error_message': error_messages.PHONE_NUMBER_ALREADY_IN_USE})
        # Validate the phone number using Twilio's lookup
        account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
        auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
        if not is_real_phone_number(phone_number, account_sid, auth_token):
            return JsonResponse({'success': False, 'error_message': error_messages.INVALID_PHONE})
        # Generate verification code and send it via SMS
        verification_code = generate_verification_code()
        request.session["phone_verification_code"] = verification_code
        request.session.set_expiry(timedelta(minutes=2))
        send_code_via_phone(verification_code,receiver=phone_number,account_sid=account_sid,auth_token=auth_token)
        # Redirect to the verification page
        return JsonResponse({
            'success': True,'redirect_url': reverse('handle_verification_code', kwargs={'email_or_phone': phone_number})
        })

    return render(request, "account/enter_new_phone_number.html")


@login_required
def handle_verification_code(request, email_or_phone):
    if request.method == "POST":
        current_user = request.user
        if not current_user:
            return JsonResponse({'success': False, 'error_message': error_messages.GENERAL_ERROR})
        code = request.POST.get("code")
        if not code:
            return JsonResponse({'success': False, 'error_message': error_messages.REQUIRED_CODE})
        if "phone_verification_code" in request.session and code == request.session["phone_verification_code"]:
            current_user.phone = email_or_phone
            del request.session["phone_verification_code"]
        elif "email_verification_code" in request.session and code == request.session["email_verification_code"]:
            current_user.email = email_or_phone
            del request.session["email_verification_code"]
        else:
            return JsonResponse({'success': False, 'error_message': error_messages.INVALID_CODE})
        current_user.save()
        return JsonResponse({'success': True})
    else:
        return render(request, "account/enter_verification_code.html")



@login_required
def view_address(request):
    current_user = request.user

    address_list = Address.objects.filter(user=current_user).all()
    return render(request, "account/address.html", {"address_list": address_list})


@login_required
def create_address(request):
    current_user = request.user

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        phone_number = request.POST.get("phone_number")
        street_address = request.POST.get("street_address")
        locality = request.POST.get("locality")
        country = request.POST.get("country")
        postal_code = request.POST.get("postal_code")
        type = request.POST.get("type")
        city = request.POST.get("city")
        is_default = request.POST.get("is_default",False)
        print(is_default)
        # Check if all required fields are provided
        required_fields = [full_name, phone_number, country, street_address, locality, postal_code, type, city]
        if all(required_fields):
            # Get the existing default address, if any
            # Create a new address instance
            new_address = Address.objects.create(
                user=current_user,
                full_name=full_name,
                phone_number=phone_number,
                street_address=street_address,
                locality=locality,
                city=city,
                postal_code=postal_code,
                country=country,
                type=type,
                is_default=is_default
            )
            new_address.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error_message': error_messages.MISSING_FIELDS})

    return render(request, "account/address_manage.html",{"is_update": False})

@login_required
def update_address(request,id):
    current_user = request.user
    address = Address.objects.filter(user=current_user, pk=id).first()
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        phone_number = request.POST.get("phone_number")
        street_address = request.POST.get("street_address")
        locality = request.POST.get("locality")
        country = request.POST.get("country")
        postal_code = request.POST.get("postal_code")
        type = request.POST.get("type")
        city = request.POST.get("city")
        is_default = request.POST.get("is_default", False)
        required_fields = [full_name, phone_number, country, street_address, locality, postal_code, type, city]
        if all(required_fields):
            address.full_name= full_name
            address.phone_number = phone_number
            address.street_address = street_address
            address.locality= locality
            address.country = country
            address.postal_code = postal_code
            address.type = type
            address.is_default = is_default
            address.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error_message': error_messages.MISSING_FIELDS})
    return render(request, "account/address_manage.html", {"address": address, "is_update": True})

@login_required
def delete_address(request, id):
    current_user = request.user
    address = Address.objects.filter(user=current_user, pk=id).first()
    address.delete()
    return redirect(reverse("view_address"))


@login_required
def change_password(request):
    current_user = request.user
    current_password = current_user.password
    if request.method == "POST":
        password = request.POST.get("password")
        if password and check_password(password, current_password):
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error_message': error_messages.INVALID_CURRENT_PASSWORD})
    return render(request, "account/enter_current_password.html")


@login_required
def set_new_password(request):
    current_user = request.user
    if request.method == "POST":
        new_password = request.POST.get("password")

        if new_password and not check_password(new_password, current_user.password):
            current_user.set_password(new_password)
            current_user.save()
            update_session_auth_hash(request, current_user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error_message': error_messages.PASSWORDS_MUST_DIFFERENT})
    return render(request, "account/enter_new_password.html")


@login_required
def view_account_notifications(request):
    current_user = request.user
    if request.method == "POST":
        checked = request.POST.get("email_notification", False)
        if checked:
            current_user.receive_updates = True
            current_user.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'error_message': error_messages.GENERAL_ERROR})
    return render(
        request,
        "account/notification_setting.html",
        {"receive_updates": current_user.receive_updates},
    )


def register_employee(request):
    if request.method == "POST":
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")

        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        if not (first_name and last_name and email and phone and username):
            return JsonResponse({'success': False, 'error_message': error_messages.MISSING_FIELDS})
        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'error_message': error_messages.USERNAME_IS_TAKEN})
        else:

            new_user = User.objects.create(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                is_active=False,
            )
            new_user.save()
            Employee.objects.create(user=new_user).save()
            return JsonResponse({'success': True})
    return render(request, "account/register_employee.html")



def reset_password(request):
    if request.method == "POST":
        email_or_phone = request.POST.get("email_or_phone")
        if not email_or_phone:
            messages.error(
                request,
                "Please provide your email or phone number to reset your password",
            )
            return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
        else:
            if is_phone_number(email_or_phone):
                if User.objects.filter(phone=email_or_phone).first():
                    verification_code = generate_verification_code()
                    request.session["phone_verification_code"] = verification_code
                    # Set session expiry to 2 minutes from now
                    request.session.set_expiry(timedelta(minutes=2))
                    if not phone_number.startswith("+"):
                        phone_number = "+84" + phone_number[1:]
                    send_code_via_phone(verification_code, phone_number)
                    return redirect(
                        reverse(
                            "handle_verification_code_reset_password",
                            kwargs={"email_or_phone": email_or_phone},
                        )
                    )
                messages.error(request, "Phone number not recognized!")
                return redirect(reverse("reset_password"))
            if is_email(email_or_phone):
                if User.objects.filter(email=email_or_phone).first():
                    code = generate_verification_code()
                    request.session["email_verification_code"] = code
                    # Set session expiry to 10 minutes from now
                    request.session.set_expiry(timedelta(minutes=10))
                    send_specific_email(
                        request=request,
                        choice=3,
                        email_list=[email_or_phone],
                        code=code,
                    )
                    return redirect(
                        reverse(
                            "handle_verification_code_reset_password",
                            kwargs={"email_or_phone": email_or_phone},
                        )
                    )
            return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
    else:
        return render(request, "account/reset_password.html")


def handle_verification_code_reset_password(request, email_or_phone):
    if request.method == "POST":
        if request.session.get("phone_verification_code"):
            print(
                f'phone_verification_code: {request.session.get("phone_verification_code")}'
            )
            user = User.objects.filter(phone=email_or_phone).first()
            print(f"phone: {user.id}")
            if (
                request.POST.get("code")
                == request.session.get("phone_verification_code")
                and user
            ):

                return redirect(
                    reverse("set_new_password_reset_password"),
                    kwargs={"user_id": user.id},
                )
        elif request.session.get("email_verification_code"):
            print(
                f'email_verification_code: {request.session.get("email_verification_code")}'
            )
            user = User.objects.filter(email=email_or_phone).first()
            print(f"email: {user.id}")
            if (
                request.POST.get("code")
                == request.session.get("email_verification_code")
                and user
            ):

                return redirect(
                    reverse("set_new_password_reset_password"),
                    kwargs={"user_id": user.id},
                )

    else:
        return render(request, "account/enter_verification_code.html")


def set_new_password_reset_password(request, user_id):
    if request.method == "POST":
        user = get_object_or_404(User, id=user_id)
        print(user)
        new_password = request.POST.get("password")
        if new_password and not check_password(new_password, user.password):
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            return redirect(reverse("index"))
        else:
            messages.error(
                request, "New password must be different from the old password!"
            )
            return redirect(reverse("set_new_password"))
    return render(request, "account/enter_new_password.html")
