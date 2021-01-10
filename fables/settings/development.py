"""
This module provides the Django settings for **fables** unique to the development environment.

"""

# Disabling 'wildcard-import' and 'unused-wildcard-import' warnings by pylint
# for this module.

# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import

from .base import *

# Django Debug Toolbar
# https://django-debug-toolbar.readthedocs.io/en/latest/

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = [
    '127.0.0.1',
]

# Email
# https://docs.djangoproject.com/en/3.0/topics/email/#email-backends

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
