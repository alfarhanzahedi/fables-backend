"""
This module provides the different ``models`` pertaining to the ``payments`` app.

"""

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import UserCoupon
from apps.organizations.models import Organization

class Payment(models.Model):
    """
    ``Payment`` is the model representing the information related to each payment.

    Attributes:
        user: A ``models.ForeignKey`` representing the user who made the payment.
        organization: A ``models.ForeignKey`` representing the organization to which the payment is made.
        user_coupon: A ``models.OneToOneField`` representing the coupon (if any) associated with the payment.

        amount: A ``models.PositiveIntegerField`` representing the amount paid.

        created_at: A ``models.DateTimeField`` representing the date and time when the instance was created.
        updated_at: A ``models.DateTimeField`` representing the date and time when the instaince was updated.

    """

    user = models.ForeignKey(
        get_user_model(), related_name='payments',
        null=True, on_delete=models.SET_NULL, verbose_name=_('User')
    )

    organization = models.ForeignKey(
        Organization, related_name='payments',
        null=True, on_delete=models.SET_NULL, verbose_name=_('Organization')
    )

    user_coupon = models.OneToOneField(
        UserCoupon, on_delete=models.SET_NULL,
        null=True, blank=True, verbose_name=_('User coupon')
    )

    amount = models.PositiveIntegerField(verbose_name=_('Amount'))

    created_at = models.DateTimeField(verbose_name=_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('Updated at'), auto_now=True)
