"""
Django settings for transaction_logging project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path
from cfenv import AppEnv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"
STATICFILES_DIRS = (os.path.join(PROJECT_DIR, "static"),)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
# Default to False unless environment variable is present
_DJANGO_DEBUG_OPTION = False
if "DJANGO_DEBUG" in os.environ:
    _DJANGO_DEBUG_OPTION = os.environ["DJANGO_DEBUG"]

DEBUG = _DJANGO_DEBUG_OPTION

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "transaction_logging_api.apps.TransactionLoggingApiConfig",
    "rest_framework",
]

if DEBUG:
    INSTALLED_APPS += (
        # Dev extensions
        "django_extensions",
    )

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "transaction_logging.urls"

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

WSGI_APPLICATION = "transaction_logging.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# The VCAP_APPLICATION environment variable is set by cloud.gov and
# populated with service information needed to connect to the database.
VCAP_ENV_VAR = "VCAP_APPLICATION"

if VCAP_ENV_VAR in os.environ:
    # Deployment to Cloud.gov -- Set DB to RDS
    ENV = AppEnv()
    RDS_VARS = ENV.get_service(label="aws-rds")
    DB_INFO = RDS_VARS.credentials

    DB_DICT = {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": DB_INFO["db_name"],
        "USER": DB_INFO["username"],
        "PASSWORD": DB_INFO["password"],
        "HOST": DB_INFO["host"],
        "PORT": DB_INFO["port"],
    }
else:
    # Local development -- use local DB info
    DB_DICT = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }

DATABASES = {"default": DB_DICT}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"
