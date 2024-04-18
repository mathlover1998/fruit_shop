from django.urls import path
from . import views

urlpatterns= [
    path('',views.view_user_account,name='view_user_account'),
    path('register/',views.register_customer,name='register_customer'),
    path('register/email/',views.collect_customer_registration_email,name='collect_customer_registration_email'),
    path('login/',views.handle_login,name='handle_login'),
    path('logout/',views.handle_logout,name='handle_logout'),
    path('profile/',views.update_profile,name='update_profile'),
    path('email/',views.update_email,name='update_email'),#
    path('phone/',views.update_phone,name='update_phone'),
    path('address/',views.view_address,name='view_address'),
    path('address/create/',views.create_address,name='create_address'),
    path('address/update/<int:id>',views.update_address,name='update_address'),
    path('address/delete/<int:id>',views.delete_address,name='delete_address'),
    path('change-password/',views.change_password,name='change_password'),
    path('change-password/confirm/',views.set_new_password,name='set_new_password'),#
    path('notification/',views.view_account_notifications,name='view_account_notifications'),
    path('register/employee/',views.register_employee,name='register_employee'),
    path('reset-password/',views.reset_password,name='reset_password'),
    path('verification-code/<str:email_or_phone>/',views.handle_verification_code,name='handle_verification_code'),#
]