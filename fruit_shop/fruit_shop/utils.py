import random, string, os
from twilio.rest import Client
from django.core.mail import send_mail
import re
# from django.template.loader import render_to_string
# from django.utils.html import strip_tags

def mask_email(email):
    if '@' in email:
        username, domain = email.split('@')
        masked_username = username[:2] + '*' * (len(username) - 4) + username[-2:]
        return masked_username + '@' + domain
    else:
        return email
    
def validate_mask_phone(phone):
    if phone is not None:
        return '*' * (len(phone) - 2) + phone[-2:]
    else:
        return 'Phone is not avaiable'
    
def generate_verification_code():
    return ''.join(random.choices(string.digits, k=6))

def send_code_via_phone(code,receiver):
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    client = Client(account_sid,auth_token)
    # html_message = render_to_string('letters/verification_email.html',{'code':code})
    # plain_message = strip_tags(html_message)
    message = client.messages.create(
        body = f'Fruitshop: Your verification code is:{code}',
        from_=os.environ.get('TWILIO_SENDER_PHONE'),
        to=f'{receiver}'
    )
    print("Message SID:", message.sid)

# def send_via_email(subject,message,from_email,email_list):
#     send_mail(subject, me, from_email, [email], html_message=html_message)

def validate_password(password):
    # Check length (between 8 and 16 characters)
    if not 8 <= len(password) <= 16:
        return False
    
    # Check for at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        return False
    
    # Check for at least one lowercase letter
    if not re.search(r'[a-z]', password):
        return False
    
    # Check for at least one normal symbol (non-alphanumeric)
    if not re.search(r'[!@#$%^&*()_+{}|:"<>?`\-=[\];\',./]', password):
        return False
    
    return True


def generate_random_password(length=12):
    characters = string.digits  # Only numbers
    return ''.join(random.choice(characters) for _ in range(length))