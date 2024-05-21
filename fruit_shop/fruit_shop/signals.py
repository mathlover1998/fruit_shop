from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from fruit_shop_app.models import Employee,User,Discount
from django.contrib.auth.hashers import make_password
from .utils import generate_random_password
from django.contrib.contenttypes.models import ContentType
from django.db import models

@receiver(post_save,sender=User)
def user_approval_notification(sender, instance, created, **kwargs):
    if not created and instance.is_approved:
        try:
            employee = Employee.objects.get(user=instance)
            new_password = generate_random_password()
            instance.password = make_password(new_password)
            instance.save()
            make_password()
            send_mail(
                'Account approved',
                f'Your account has been approved. Your password is: {new_password}',
                settings.EMAIL_HOST_USER,  # sender's email
                [instance.email],  # recipient's email
                fail_silently=False,
            )
        except Employee.DoesNotExist:
            pass



