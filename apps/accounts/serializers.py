"""
This module provides the different ``serializers`` pertaining to the ``accounts`` app.

"""

from django.contrib.auth import get_user_model

from rest_framework import serializers

import apps.accounts.constants as constants

# Disabling 'abstract-method' warning by pylint for this module.
# pylint: disable=abstract-method

class EmailSerializer(serializers.Serializer):
    """
    ``EmailSerializer`` is used to serialize the request data (containing ``email``)
    for generation of an OTP(:class:`apps.models.OTP`) code (to enable sign-in/sign-up).

    Attributes:
        email: A ``serializers.EmailField`` to serialize and validate the ``email`` present in
        the request data.

    """

    email = serializers.EmailField(
        required=True,
    )

class OTPCodeSerializer(serializers.Serializer):
    """
    ``OTPCodeSerializer`` is used to serialize the request data containing an OTP(:class:`apps.models.OTP`)
    ``code``.

    Attributes:
        code: A ``serializers.CharField`` to serialize and validate the OTP(:class:`apps.models.OTP`) ``code``
              present in the request data.

    """

    code = serializers.CharField(
        required=True,
        min_length=constants.OTP_CODE_LENGTH,
        max_length=constants.OTP_CODE_LENGTH
    )

class UserSerializer(serializers.ModelSerializer):
    """
    ``UserSerializer`` is used to serialize an instance of :class:`apps.accounts.models.User`.

    """

    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name', 'email', 'profile_picture')
        read_only_fields = ('id', 'email')
