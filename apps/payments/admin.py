"""
This module provides the different admin functionalities pertaining to
the ``payments`` app.

"""

from django.contrib import admin

from apps.payments.models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """
    ``PaymentAdmin`` provides the different admin functionalities and features
    for the model - :class:`apps.payments.models.Payment`.

    """
