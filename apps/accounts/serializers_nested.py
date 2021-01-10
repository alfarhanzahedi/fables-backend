"""
This module provides the different nested ``serializers`` pertaining to the ``accounts`` app.

"""

from rest_framework import serializers

from apps.accounts.models import UserCoupon
from apps.organizations.serializers import OrganizationSerializer

# Disabling 'abstract-method' warning by pylint for this module.
# pylint: disable=abstract-method

class UserCouponSerializer(serializers.ModelSerializer):
    """
    ``UserCouponSerializer`` is used to serialize an instance of :class:`apps.accounts.models.Coupon`.

    """
    organization = OrganizationSerializer(read_only=True)

    class Meta:
        model = UserCoupon
        fields = '__all__'
