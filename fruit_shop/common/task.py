# from celery import shared_task
# from django.contrib.auth.models import User
# from datetime import datetime, timedelta

# @shared_task
# def delete_accounts_without_email():
#     # Delete accounts without an email field created more than 5 minutes ago
#     cutoff_time = datetime.now() - timedelta(minutes=5)
#     User.objects.filter(email='', date_joined__lte=cutoff_time).delete()