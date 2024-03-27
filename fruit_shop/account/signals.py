from django.db.models.signals import pre_save
from django.dispatch import receiver
from fruit_shop_app.models import User,Employee
from django.core.mail import send_mail
from django.conf import settings
from fruit_shop.utils import generate_random_password
# from django.contrib.auth.hashers import make_password

@receiver(pre_save,sender=User)
def employee_approval_notification(sender,instance, **kwargs):
    if instance.is_approved and Employee.objects.filter(user=instance).first():
        new_password = generate_random_password()
        instance.set_password(new_password)
        instance.is_active = True
        send_mail(
            'Account Approved',
            f'Your account has been approved.Your password is: {new_password}',
            settings.EMAIL_HOST_USER,  # sender's email
            [instance.email],  # recipient's email
            fail_silently=False,
        )