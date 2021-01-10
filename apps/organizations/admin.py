"""
This module provides the different admin functionalities pertaining to
the ``organizations`` app.

"""

from django.contrib import admin

from apps.organizations.models import Organization
from apps.organizations.models import Review

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """
    ``OrganizationAdmin`` provides the different admin functionalities and features
    for the model - :class:`apps.organizations.models.Organization`.

    """

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    ``ReviewAdmin`` provides the different admin functionalities and features
    for the model - :class:`apps.organizations.models.Review`.

    """
