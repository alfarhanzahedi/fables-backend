"""
This module provides the different admin functionalities pertaining to
the ``accounts`` app.

"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from apps.accounts.models import User

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """
    ``UserAdmin`` inherites ``django.contrib.auth.admin`` and provides the different admin
    functionalities and features for the custom user model - :class:`apps.accounts.models.User`.

    """
