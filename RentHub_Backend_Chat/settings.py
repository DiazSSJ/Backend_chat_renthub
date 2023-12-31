"""
Django settings for RentHub_Backend_Chat project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import dj_database_url
import os

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = os.environ.get("SECRET_KEY")
#SECRET_KEY = 'AKKDVkdsmvlsvmrebve5b5dv1svws'

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = os.environ.get("DEBUG", "False").lower() == "true"
#DEBUG = True

ALLOWED_HOSTS = ['*']
#ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(" ")




# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    'corsheaders',
    'coreapi',
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'microservice_chat',
    'rest_framework',
    'elasticapm.contrib.django'
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'elasticapm.contrib.django.middleware.TracingMiddleware'
]

ROOT_URLCONF = "RentHub_Backend_Chat.urls"

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

WSGI_APPLICATION = "RentHub_Backend_Chat.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

database_url = os.environ.get("DATABASE_URL")
DATABASES["default"] =  dj_database_url.parse(database_url)

#DATABASES["default"] =  dj_database_url.parse("postgres://backend_chat_db_user:QpT4cE8mx8shhwmLlR8NLZF93ynRxkaa@dpg-ckuov9ub0mos73cjl0fg-a.ohio-postgres.render.com/backend_chat_db")

#postgres://backend_chat_db_user:QpT4cE8mx8shhwmLlR8NLZF93ynRxkaa@dpg-ckuov9ub0mos73cjl0fg-a.ohio-postgres.render.com/backend_chat_db

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

CORS_ALLOWED_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = ['*',]

CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',  # Agrega aquí tus dominios permitidos
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

ELASTIC_APM = {
  'SERVICE_NAME': 'renthub_chat_backend',

  'SECRET_TOKEN': 'BgqkrxPiNnk6MmnOkl',

  'SERVER_URL': 'https://17753c254e824399b755a1a7f8dd9573.apm.us-central1.gcp.cloud.es.io:443',

  'ENVIRONMENT': 'chat-environment',

  'DEBUG': True,

  'ELASTIC_APM_USE_STRUCTLOG' : True
}

formatstring = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
formatstring = formatstring + " | elasticapm " \
                              "transaction.id=%(elasticapm_transaction_id)s " \
                              "trace.id=%(elasticapm_trace_id)s " \
                              "span.id=%(elasticapm_span_id)s"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s - %(asctime)s - %(module)s - %(message)s - %(levelname)s'
        },
        'elastic': {
            'format': formatstring
        }
    },
    'handlers': {
        'elasticapm': {
            'level': 'INFO',
            'class': 'elasticapm.contrib.django.handlers.LoggingHandler',
            'formatter': 'verbose'
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        "django": {
            "handlers": ["console", "elasticapm"],
            "level": "INFO",
        },
        # Log errors from the Elastic APM module to the console (recommended)
        'elasticapm.errors': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}
