from pathlib import Path
import os
from datetime import timedelta
from decouple import config
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-l9j&#9l^5u8h)2h9wc)nii413@n)q*7jjoae2_6zi)u7$r))4u'

DEBUG = True


ALLOWED_HOSTS = [
    "raximov.pythonanywhere.com",
    "localhost",
    "127.0.0.1",
]

CORS_ALLOWED_ORIGINS = [
    "https://raximov.pythonanywhere.com",
    "http://localhost:8080",
    "http://127.0.0.1:9000",
]

# settings.py
STRIPE_SECRET_KEY = 'sk_test_51PjcRqIIDOuV803oBQ4VljZWNCOdh5Z9ttQ6fGLy7XKOy86Xv8JfnkUqixIwu9f2p8O9mKUn8NO2WQ6OodMvk0yc00kjVD7kIR'
STRIPE_PUBLISHABLE_KEY = 'pk_test_51PjcRqIIDOuV803oOlf5PdqU3Boh0pmVRdb1pQGVqUnwwZ2j7xPhi25N0Yv46ETzZ10AKuegQXcshOq3z0KM3LIN00xn7sY8St'



INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_spectacular',
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',
    "corsheaders",

    # locale apps
    "cafe.apps.CafeConfig",
    "users.apps.UsersConfig",
    "order.apps.OrderConfig",
    "payment.apps.PaymentConfig"

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Midas Project\'s API',
    'DESCRIPTION': 'The backend part was developed by Aslonbek',
    'VERSION': '1.0.0',
    # Qo'shimcha sozlamalar kerak bo'lsa, qo'shishingiz mumkin
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=10),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=190),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}



# WSGI_APPLICATION = 'core.wsgi.application'
ASGI_APPLICATION = 'core.asgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'quiz',   # PostgreSQL dagi ma'lumotlar bazasi nomi
#         'USER': 'arslon',   # PostgreSQL foydalanuvchi nomi
#         'PASSWORD': '110701',  # PostgreSQL paroli
#         'HOST': 'localhost',  # Agar PostgreSQL konteyneri o'ziga xos IP manzilida bo'lsa, 'HOST' ni u o'rniga qo'ying
#         'PORT': '5432',       # PostgreSQL porti
#     }
# }


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



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_TZ = True

# Client modeli
AUTH_USER_MODEL = 'users.ClientModel'

# Media sozlamalari
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Static sozlamalari
STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'




EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')