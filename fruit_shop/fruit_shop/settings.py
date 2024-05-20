"""
Django settings for fruit_shop project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-(py9y)mt4nwsukdwcye0nm95i_+*0__s32oe-!2a_@g+!4pekk'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]

# CELERY_BROKER_URL = 'django://'
# CELERY_RESULT_BACKEND = 'django-db'

LOGIN_URL = '/account/login/'

EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND')
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', '').lower() == 'true'  # Convert to bool
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # "whitenoise.runserver_nostatic",
    'django.contrib.staticfiles',
    'fruit_shop_app',
    'account',
    'product_manager',
    'blog',
    'common',
    'storages',
    # 'django_celery_beat'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'fruit_shop.middleware.CustomPermissionDeniedMiddleware',
    'fruit_shop.middleware.CheckURLMiddleware',
    'fruit_shop.middleware.CheckProductExistMiddleware',
    
]

ROOT_URLCONF = 'fruit_shop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'fruit_shop_app/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'common.context_processors.get_global_cart_data',
                'common.context_processors.get_separated_category_product',
                'common.context_processors.get_category_name_context',
                'common.context_processors.get_latest_discounts',
                'common.context_processors.get_website_information',
                'common.context_processors.get_featured_products_context',
                'common.context_processors.get_recently_viewed_products',
                'common.context_processors.get_domain_name',
            ],
            'libraries':{
                'custom_filters': 'common.custom_filters'
            }
        },
    },
]

WSGI_APPLICATION = 'fruit_shop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# local postgresql database
# DATABASES = {
    
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'fruit_shop_db',
#         'USER': 'admin',
#         'PASSWORD': '1234',
#         'HOST':'localhost',
#         'PORT':'5432' 
#     }
# }


# aws database (disabled)
# DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': 'cole_fruit_shop_db',
    #     'USER': 'coletran',
    #     'PASSWORD': 'Bunnie123',
    #     'HOST':'database-2.clbdt0uzsyg9.ap-southeast-2.rds.amazonaws.com',
    #     'PORT':'5432' 
    # }
# }


#render database
DATABASES = {
    
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        **dj_database_url.config(default=os.environ.get('DATABASE_URL'))
    }
}
    



# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'fruit_shop_app.User'




# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "fruit_shop_app/static"),
)

# STORAGES = {
#     "staticfiles": {
#         "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
#     },
# }

MEDIA_ROOT = os.path.join(BASE_DIR,'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# WHITENOISE_MANIFEST_STRICT = False
# STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"
# STATICFILES_STORAGE="whitenoise.storage.CompressedManifestStaticFilesStorage"

#AWS configuration
AWS_ACCESS_KEY_ID=os.environ.get('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY=os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'cole-grocery-shop-98'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_FILE_OVERWRITE = False

STORAGES = {

    # Media file (image) management   
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
    },
    
    # CSS and JS file management
    "staticfiles": {
        "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
    },
}