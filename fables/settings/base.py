"""
This module provides the Django settings for **fables**, common to both the
environments - development and production.

"""

import os

import dj_database_url
from decouple import config
from decouple import Csv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',

    'apps.accounts',
    'apps.organizations',
    'apps.payments'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'apps.accounts.middleware.CSRFMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'fables.urls'

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

WSGI_APPLICATION = 'fables.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.parse(config('DEFAULT_DATABASE_URL')),
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATIC_URL = '/static/'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Media files
# https://docs.djangoproject.com/en/3.0/ref/settings/#std:setting-MEDIA_ROOT

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# Custom model used to represent a User.
# https://docs.djangoproject.com/en/3.0/ref/settings/#std:setting-AUTH_USER_MODEL

AUTH_USER_MODEL = 'accounts.User'


# Logging
# https://docs.djangoproject.com/en/3.0/topics/logging/

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] %(levelname)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'development_logfile': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.FileHandler',
            'filename': 'logs/development.log',
            'formatter': 'verbose'
        },
        'production_logfile': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/production.log',
            'maxBytes' : 1024 * 1024 * 5,
            'backupCount' : 5,
            'formatter': 'simple'
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console'],
    },
    'loggers': {
        'apps': {
            'handlers': ['development_logfile', 'production_logfile'],
        },
        'django': {
            'handlers': ['development_logfile', 'production_logfile'],
        },
        'py.warnings': {
            'handlers': ['development_logfile'],
        },
    }
}


# A list of origins that are authorized to make cross-site HTTP requests to this application.
# https://github.com/adamchainz/django-cors-headers

CORS_ORIGIN_WHITELIST = config('CORS_ORIGIN_WHITELIST', cast=Csv())


# Should allow credentials?
# https://github.com/adamchainz/django-cors-headers
CORS_ALLOW_CREDENTIALS = True


# Django REST framework
# https://www.django-rest-framework.org/

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'EXCEPTION_HANDLER': 'utils.exception_handler.exception_handler',
}


# A dictionary of response statuses that any of the API calls will return, as per the specification
# specified at https://github.com/omniti-labs/jsend.

API_RESPONSE_STATUS = {
    'FAIL': 'fail',
    'SUCCESS': 'success',
    'ERROR': 'error'
}

# Documentation string for API_RESPONSE_STATUS defined above.
"""
A dictionary of response statuses that any of the API calls will return, as per the specification
specified at https://github.com/omniti-labs/jsend.
::

    API_RESPONSE_STATUS = {
        'FAIL': 'fail',
        'SUCCESS': 'success',
        'ERROR': 'error'
    }

"""

MLDB_DB_PATH = os.path.join(BASE_DIR, 'logs')
