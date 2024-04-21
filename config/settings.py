# flake8: noqa
"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from datetime import timedelta
from corsheaders.defaults import (
    default_headers,
)
from environ import Env

SITE_ID = 1

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


ENV_FILE = ".env"
ENV_FILE_PATH = BASE_DIR / ENV_FILE

Env.read_env(ENV_FILE_PATH)
env = Env()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "corsheaders",
    "phonenumber_field",
    "rest_framework",
    "rest_framework.authtoken",
    "drf_spectacular",
    "knox",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.mfa",
    "api.common",
    "api.authentication",
    "api.users",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

ROOT_URLCONF = "config.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Mail
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = "foo@bar.com"

# User Model
AUTH_USER_MODEL = "users.UserModel"

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# CORS
CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_HEADERS = (
    *default_headers,
    "X-Session-Token",
    "location",
)

# Rest Framework
REST_FRAMEWORK = {
    # API Versioning
    "DEFAULT_VERSION": "v1",
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.AcceptHeaderVersioning",
    # Auth
    "DEFAULT_AUTHENTICATION_CLASSES": (
        'knox.auth.TokenAuthentication',
    ),
    # Exception
    "EXCEPTION_HANDLER": "api.common.exceptions.handler",
    # Pagination
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.CursorPagination",
    "PAGE_SIZE": 15,
    # Test
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    # Docs
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}


# Knox (For Auth Token Management)
REST_KNOX = {
    "TOKEN_TTL": timedelta(days=20),
    "AUTH_HEADER_PREFIX": "Bearer",
}
KNOX_TOKEN_MODEL = "knox.AuthToken"


# All-Auth
ACCOUNT_ADAPTER = "api.authentication.adapter.AccountAdapter"
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "optional"
ACCOUNT_CHANGE_EMAIL = True
ACCOUNT_EMAIL_NOTIFICATIONS = True
ACCOUNT_USERNAME_MIN_LENGTH = 3
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
# All-Auth : Headless
HEADLESS_TOKEN_STRATEGY = 'api.authentication.tokens.SessionTokenStrategy'

# Client (Frontend) Url Manager
CLIENT_DOMIAN = "localhost:5000"

# Twilio
TWILIO_ACCOUNT_SID = env("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = env("TWILIO_AUTH_TOKEN")
TWILIO_VERIFY_SERVICE_SID = env("TWILIO_VERIFY_SERVICE_SID")


LOGGING = {

    'version': 1,

    'disable_existing_loggers': False,

    'handlers': {

        'console': {

            'level': 'DEBUG',

            'class': 'logging.StreamHandler',

        },

        'file': {

            'level': 'DEBUG',

            'class': 'logging.FileHandler',

            'filename': 'django_queries.log',  # Choose a file name and path

        },

    },

    'loggers': {
        'django.db.backends': {

            'handlers': ['file'],

            'level': 'DEBUG',

            'propagate': False,

        },

    },
}