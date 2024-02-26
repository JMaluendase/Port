"""
Django settings for backendportal project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-mw5(2v)+-h4ot!ncecz(e7-(pk!gi(%r*6n(kq8#cl*za!3dg2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['172.16.10.20',
                 'gestor.berlinasdelfonce.com', '201.216.13.253', '127.0.0.1']

# Este es el que permitió la conexión con VUE
CORS_ORIGIN_ALLOW_ALL = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'api'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backendportal.urls'

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

WSGI_APPLICATION = 'backendportal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': 'portalv1',
    #     'USER': 'diego',
    #     'PASSWORD': 'diegojmartinezp',
    #     'HOST': '192.168.1.99',
    #     'PORT': 5432,
    # }

    # 'default': {
    #    'ENGINE': 'django.db.backends.postgresql',
    #    'NAME': 'portalv1',
    #    'USER': 'postgres',
    #    'PASSWORD': 'diegojmartinezp',
    #    'HOST': 'localhost',
    #   'PORT': 5433,
    # }


    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'GestorTIC',
        'USER': 'postgres',
        'PASSWORD': '$ZadKiel$',
        'HOST': '172.16.10.20',
        'PORT': 5445,
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Bogota'
USE_TZ = True
USE_I18N = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_HOST = "mail.berlinasdelfonce.com"
EMAIL_PORT = 465
EMAIL_HOST_USER = "noresponder@berlinave.com"
EMAIL_HOST_PASSWORD = "Noresponder.2020"
EMAIL_USE_TLS = True

MESSAGE_ERROR = "Transacción Fallida"
MESSAGE_CONFIRM = "Transacción Exitosa!"

SMS_USER = "proyectos@solincosta.com"
SMS_PASS = "xyv8t3df"

DOMAIN = "https://www.berlinave.com/pdf_extractos/"
EMAIL_PQR_RECEIVER = "proyectos@solincosta.com"