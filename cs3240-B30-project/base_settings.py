"""
Django settings for CS3240F18 project.

Generated by 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GDAL_LIBRARY_PATH = os.environ.get('GDAL_LIBRARY_PATH')
GEOS_LIBRARY_PATH = os.environ.get('GEOS_LIBRARY_PATH')
BUILD_WITH_GEO_LIBRARIES = 1

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = '8rjfrw$q8&_-v%0qifuczvtgwroa&47qk4nn709*&4*$k+@b&e'
SECRET_KEY = 'WNPYNRYkfagHeKA3dFdaCoWY'
GOOGLE_MAPS_API_KEY = 'AIzaSyCPPr47Z0_E8wR4WLD3_YrFDyCe19v4oJQ'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'bootstrap4',
    'login',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    'django_google_maps',

]

ACCOUNT_LOGOUT_ON_GET = True

# ACCOUNT_ADAPTER = "login.adapters.AccountAdapter"


SITE_ID = 3

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cs3240-B30-project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'login', 'templates'), ],
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

WSGI_APPLICATION = 'cs3240-B30-project.wsgi.application'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.contrib.gis.db.backends.postgis',
    #     #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    #     'NAME': 'd8iuuhia3hrj1s',
    #     'USER': 'gjsoixmrqogmfy',
    #     'PASSWORD': '7a902f835eb2c30caf68a0ed4a1c5a59876da460af0894824e58cc80a85a470d',
    #     'HOST': 'ec2-3-211-37-117.compute-1.amazonaws.com',
    #     'PORT': '5432',
    #     'TEST': {
    #         'NAME': 'test_db',
    #     },
    # }
    # 'default': {
    # 'ENGINE': 'django.db.backends.postgresql',
    #    'ENGINE': 'django.contrib.gis.db.backends.postgis',
    # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    #   'NAME': 'b30_db',
    #   'USER': 'pg-admin',
    #   'PASSWORD': 'HiqEuIC9cwkwsFwm',
    #   'HOST': '34.73.171.158',
    #  'PORT': '5432',
    # 'TEST': {
    #     'NAME': 'test_db',
    # },
    # }

    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'homelocation',
        'USER': 'pg-admin',
        'PASSWORD': 'HiqEuIC9cwkwsFwm',
        'HOST': '34.73.62.249',
        'PORT': '5432',
        'TEST': {
            'NAME': 'test_db',
        },
    }

    # 'default': {
    #    'ENGINE': 'django.contrib.gis.db.backends.postgis',
    #    'NAME': 'd8iuuhia3hrj1s',
    #    'USER': 'gjsoixmrqogmfy',
    #    'PASSWORD': '7a902f835eb2c30caf68a0ed4a1c5a59876da460af0894824e58cc80a85a470d',
    #    'HOST': 'ec2-3-211-37-117.compute-1.amazonaws.com',
    #    'PORT': '5432',
    #    'TEST': {
    #        'NAME': 'test_db',
    #    },
    # }

}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
]
# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_USER_MODEL = 'login.Account'
ACCOUNT_EMAIL_VERIFICATION = 'none'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

# Activate Django-Heroku.
try:
    # Configure Django App for Heroku.
    import django_heroku

    django_heroku.settings(locals())
except ImportError:
    found = False

BASE_URL = "http://127.0.0.1:8000"