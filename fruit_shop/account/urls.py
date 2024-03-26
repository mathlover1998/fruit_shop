from django.urls import path
from . import views

urlpatterns= [
    path('profile/',views.profile,name='profile'),
    path('register/',views.customer_register,name='customer_register'),
    path('register-email/',views.customer_register_email,name='customer_register_email'),
    path('sign-in/',views.signin,name='sign_in'),
    path('logout/',views.log_out,name='logout'),
    path('update-profile/',views.update_profile,name='update_profile'),
    path('update-email/',views.update_email,name='update_email'),
    path('confirm-code/<str:email>/',views.confirm_validation_code,name='confirm_validation_code'),
    path('update-phone/',views.update_phone,name='update_phone'),
    path('confirm-phone=code/<str:phone>/',views.confirm_phone_verification_code,name='confirm_phone_verification_code'),
    path('address/',views.address_view,name='address_view'),
    path('address/add/',views.create_address,name='create_address'),
    path('address/update/<int:id>',views.update_address,name='update_address'),
    path('address/delete/<int:id>',views.delete_address,name='delete_address'),
    path('change-password/',views.update_password,name='update_password'),
    path('confirm-password',views.confirm_new_password,name='confirm_new_password'),
    path('setting/notification/',views.notification_setting_view,name='notification_setting_view'),
    # path('reset/',views.reset_password,name='reset_password'),
    # path('reset/method/',views.choose_reset_method,name='choose_reset_method'),
]