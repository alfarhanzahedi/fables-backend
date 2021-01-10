"""
This module provides the Django settings for **fables** unique to the production environment.

"""

# Disabling 'wildcard-import' and 'unused-wildcard-import' warnings by pylint
# for this module.

# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import

from .base import *

# Email
# https://docs.djangoproject.com/en/3.0/topics/email/#email-backends

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_USE_TLS = config('EMAIL_USE_TLS')
