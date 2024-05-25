import random, string, os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from django.core.mail import send_mail
import re, openpyxl
from functools import wraps
from django.http import HttpResponseForbidden,HttpResponse,Http404
from fruit_shop_app.models import Employee,Category,Brand,UNIT
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import pandas as pd
from io import BytesIO
import boto3
from openpyxl.worksheet.datavalidation import DataValidation
import botocore.exceptions

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

def handle_uploaded_file(f):
    file_path = os.path.join(settings.MEDIA_ROOT, f.name)
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return file_path


def convert_to_csv(file_path):
    csv_file_path = os.path.splitext(file_path)[0] + '.csv'
    df = pd.read_excel(file_path)
    df.to_csv(csv_file_path, index=False)
    return csv_file_path


# def modify_excel_file():

#     template_path = os.path.join(settings.STATIC_ROOT, 'templates/template.xlsx')
#     workbook = openpyxl.load_workbook(template_path)
#     sheet = workbook["Product"]

#     #handle product price
#     price_dv = DataValidation(
#         type='whole',
#         operator="between",
#         formula1="0", 
#         formula2="9999999999", 
#         showErrorMessage=True
#     )
#     price_dv.error = 'Invalid input'
#     price_dv.errorTitle = 'Invalid Entry'
#     price_dv.prompt = 'Please enter a number between 0 and 999999999'
#     sheet.add_data_validation(price_dv)
#     price_dv.add("B2:B1048576")

#     #handle unit type
#     unit_names = list(unit[0] for unit in UNIT)
#     unit_dv = DataValidation(
#         type='list',
#         formula1=f'"{",".join(unit_names)}"'
#     )
#     sheet.add_data_validation(unit_dv)
#     unit_dv.add("D2:D1048576")

#     #handle stock quantity
#     stock_dv = DataValidation(
#         type='whole',
#         operator="between",
#         formula1="0", 
#         formula2="999999", 
#         showErrorMessage=True
#     )
#     stock_dv.error = 'Invalid input'
#     stock_dv.errorTitle = 'Invalid Entry'
#     stock_dv.prompt = 'Please enter a number between 0 and 999999'
#     sheet.add_data_validation(stock_dv)
#     stock_dv.add("E2:E1048576")

#     #handle brand
#     brand_names = list(Brand.objects.values_list('brand_name', flat=True))
#     brand_dv = DataValidation(
#         type="list",
#         formula1=f'"{",".join(brand_names)}"'
#     )
#     sheet.add_data_validation(brand_dv)
#     brand_dv.add("I2:I1048576")

#     #handle category
#     category_names = list(Category.objects.filter(parent_category__isnull=False).values_list('category_name', flat=True))
#     category_dv = DataValidation(
#         type="list",
#         formula1=f'"{",".join(category_names)}"'
#     )
#     sheet.add_data_validation(category_dv)
#     category_dv.add("J2:J1048576")

#     #save to new file
#     modified_template_path = os.path.join(settings.MEDIA_ROOT, 'templates/modified_template.xlsx')
#     workbook.save(modified_template_path)

#     return modified_template_path

#using it only when use s3 bucket
def modify_excel_file():
    read_object_key = "templates/product_template.xlsx"
    media_object_key = "images/products.xlsx"  # new file name

    s3_client = boto3.client('s3')

    # Get object from read bucket
    response = s3_client.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=read_object_key)
    file_content = response['Body'].read()

    # Read data from in-memory file using openpyxl
    workbook = openpyxl.load_workbook(BytesIO(file_content))
    sheet = workbook["Product"]

    price_dv = DataValidation(
        type='whole',
        operator="between",
        formula1="0", 
        formula2="9999999999", 
        showErrorMessage=True
    )
    price_dv.error = 'Invalid input'
    price_dv.errorTitle = 'Invalid Entry'
    price_dv.prompt = 'Please enter a number between 0 and 999999999'
    sheet.add_data_validation(price_dv)
    price_dv.add("B2:B1048576")

    #handle unit type
    unit_names = list(unit[0] for unit in UNIT)
    unit_dv = DataValidation(
        type='list',
        formula1=f'"{",".join(unit_names)}"'
    )
    sheet.add_data_validation(unit_dv)
    unit_dv.add("D2:D1048576")

    #handle stock quantity
    stock_dv = DataValidation(
        type='whole',
        operator="between",
        formula1="0", 
        formula2="999999", 
        showErrorMessage=True
    )
    stock_dv.error = 'Invalid input'
    stock_dv.errorTitle = 'Invalid Entry'
    stock_dv.prompt = 'Please enter a number between 0 and 999999'
    sheet.add_data_validation(stock_dv)
    stock_dv.add("E2:E1048576")

    #handle brand
    brand_names = list(Brand.objects.values_list('brand_name', flat=True))
    brand_dv = DataValidation(
        type="list",
        formula1=f'"{",".join(brand_names)}"'
    )
    sheet.add_data_validation(brand_dv)
    brand_dv.add("I2:I1048576")

    #handle category
    category_names = list(Category.objects.filter(parent_category__isnull=False).values_list('category_name', flat=True))
    category_dv = DataValidation(
        type="list",
        formula1=f'"{",".join(category_names)}"'
    )
    sheet.add_data_validation(category_dv)
    category_dv.add("J2:J1048576")
    # Implement your validation/modification logic here (modify `sheet`)
    # Example: Add a value to the first cell

    # Create new in-memory file object
    output_buffer = BytesIO()
    workbook.save(output_buffer)

    # Move the buffer cursor to the beginning
    output_buffer.seek(0)

    # Save new file to media bucket
    s3_client.put_object(Body=output_buffer.getvalue(), Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=media_object_key)
    return media_object_key

