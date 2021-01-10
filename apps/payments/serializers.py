"""
This module provides the different ``serializers`` pertaining to the ``payments`` app.

"""

from rest_framework import serializers

from apps.payments.models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    """
    ``PaymentSerializer`` is used to serialize an instance of :class:`apps.payments.models.Payment`.

    """

    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')
