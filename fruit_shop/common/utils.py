import random, string, os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from django.core.mail import send_mail
import re
from functools import wraps
from django.http import HttpResponseForbidden
from fruit_shop_app.models import Employee
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import timedelta


def is_phone_number(input_str):

    pattern = r"^(\+\d{1,2}\s?)?(\d{3}|\(\d{3}\))([\s.-]?\d{3}[\s.-]?\d{4})$"

    return re.match(pattern, input_str) is not None


def is_email(input_str):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, input_str) is not None


def mask_email(email):
    if "@" in email:
        username, domain = email.split("@")
        masked_username = username[:2] + "*" * (len(username) - 4) + username[-2:]
        return masked_username + "@" + domain
    else:
        return email


def validate_mask_phone(phone):
    if phone is not None:
        return "*" * (len(phone) - 2) + phone[-2:]
    else:
        return "Phone is not avaiable"


def generate_verification_code():
    return "".join(random.choices(string.digits, k=6))


def is_real_phone_number(phone_number, account_sid, auth_token):
    client = Client(account_sid, auth_token)
    if phone_number.startswith("0"):
        phone_number = "+84" + phone_number[1:]
    try:
        number = client.lookups.phone_numbers(phone_number).fetch()
        return True
    except Exception as e:
        print("Error:", e)
        return False


def send_code_via_phone(code, receiver, account_sid, auth_token):
    client = Client(account_sid, auth_token)
    if receiver.startswith("0"): 
        receiver = "+84" + receiver[1:]
    try:
        message = client.messages.create(
            body=f"Cole's Grocery Shop: Your verification code is:{code}",
            from_=os.environ.get("TWILIO_SENDER_PHONE"),
            to=f"{receiver}",
        )
    except TwilioRestException as e:
        print("An error was occurred: ", e)


def send_specific_email(request, choice: int, email_list, code=""):
    subject, message = "", ""
    from_email = os.environ.get("EMAIL_HOST_USER")
    # welcome mail
    if choice == 1:
        subject = "Cole's Grocery Shop: Welcome to Grocery Shop"
        message = "Congratulations on your successful registration"
    # receive updates mail
    elif choice == 2:
        subject = (
            "Cole's Grocery Shop: Thank you for subscribing to the Grocery Shop newsletter"
        )
        html_message = render_to_string(
            "letters/receive_updates.html", {"user": request.user.username}
        )
        message = strip_tags(html_message)
    # mail with 6-digits verification code
    elif choice == 3:
        subject = f"Verification Code: {code}"
        html_message = render_to_string(
            "letters/verification_email.html",
            {"user": request.user.username, "code": code},
        )
        message = strip_tags(html_message)
    #receive newsletter    
    elif choice==4:
        subject = (
            "Cole's Grocery Shop: Notification"
        )
        message = "Thank you for contacting us! We will respond to your inquiry as soon as possible."
        
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=email_list,
        fail_silently=True,
    )


def validate_password(password):
    # Check length (between 8 and 16 characters)
    if not 8 <= len(password) <= 16:
        return False

    # Check for at least one uppercase letter
    if not re.search(r"[A-Z]", password):
        return False

    # Check for at least one lowercase letter
    if not re.search(r"[a-z]", password):
        return False

    # Check for at least one normal symbol (non-alphanumeric)
    if not re.search(r'[!@#$%^&*()_+{}|:"<>?`\-=[\];\',./]', password):
        return False

    return True


def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))


def replace_string(value, new):
    new_words = value.replace("_count", new)
    words = new_words.split("_")
    return " ".join(word.capitalize() for word in words)


def position_required(*positions):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                try:
                    employee = request.user.employee
                except Employee.DoesNotExist:
                    return HttpResponseForbidden(
                        "You don't have permission to access this page."
                    )
                if employee.position in positions:
                    return view_func(request, *args, **kwargs)
            return HttpResponseForbidden(
                "You don't have permission to access this page."
            )

        return _wrapped_view

    return decorator


def role_required(allowed_roles=[]):
    """
    Decorator to restrict access to users with specific roles.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if (
                request.user.is_authenticated
                and request.user.groups.filter(name__in=allowed_roles).exists()
            ):
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden(
                    "You don't have permission to access this page."
                )

        return _wrapped_view

    return decorator
