"""
This module provides the different ``models`` pertaining to the ``accounts`` app.

"""

from django.db import models
from django.utils.crypto import get_random_string
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

import apps.accounts.constants as constants
from utils.helpers import get_upload_path

class User(AbstractUser):
    """
    ``User`` inherits ``django.contrib.auth.model.AbstractUser`` and is the model for a user of
    the application.

    It is also used as the ``AUTH_USER_MODEL`` of the application.

    Attributes:
        profile_picture: A ``model.ImageField`` representing the profile picture of the user.

    """

    profile_picture = models.ImageField(
        verbose_name=_('Profile picture'), upload_to=get_upload_path,
        null=True, blank=True
    )


class OTP(models.Model):
    """
    ``OTP`` is the model required to implement a **passwordless** sign-in/signup functionality.

    Attributes:
        user: A ``models.ForeignKey`` field repsenting the user whose
              OTP is been referred to.

        code: A ``models.CharField`` for a unique random string functioning as the
              OTP code for the :py:attr:`user`.

        created_at: A ``models.DateTimeField`` for the date and time when the instance was created.
        updated_at: A ``models.DateTimeField`` for the date and time when the instance was updated
                    (the :py:attr:`code` was used or expired).

        is_used: A `models.BooleanField`` - ``True`` if the :py:attr:`code` was used, else ``False``.
        is_expired: A ``models.BooleanField`` - ``True`` if the :py:attr:`code` was expired, else ``False``.

    """

    user = models.ForeignKey(
        get_user_model(), related_name='otp',
        on_delete=models.CASCADE, verbose_name=_('User')
    )
    code = models.CharField(
        verbose_name=_('Code'), max_length=constants.OTP_CODE_LENGTH,
        unique=True, db_index=True
    )
    created_at = models.DateTimeField(verbose_name=_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('Updated at'), auto_now=True)
    is_used = models.BooleanField(verbose_name=_('Is used?'), default=False)
    is_expired = models.BooleanField(verbose_name=_('Is expired?'), default=False)

    class Meta:
        verbose_name = _('OTP')
        verbose_name_plural = _('OTPs')

    # Disabling 'arguments-differ' warning by pylint.
    # See: https://github.com/PyCQA/pylint-django/issues/94
    # pylint: disable=arguments-differ

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = get_random_string(constants.OTP_CODE_LENGTH)
        return super().save(*args, **kwargs)



# Organization references User. Hence, it should be imported after the definition of User.
# pylint: disable=wrong-import-position
from apps.organizations.models import Organization

class UserVisitHistory(models.Model):
    """
    ``UserVisitHistory`` is the model representing the visit history of a user.

    Attributes:
        user: A ``models.ForeignKey`` field repsenting the user whose
              visited an organization.
        organization: A ``models.ForeignKey()`` representing the organization visited by the user.
        visited_on: A ``models.DateTimeField()`` representing the date and time when the user
                    visited the organization.

    """

    user = models.ForeignKey(
        get_user_model(), related_name='visit_history',
        on_delete=models.CASCADE, verbose_name=_('User')
    )
    organization = models.ForeignKey(
        Organization, related_name='users_visited',
        on_delete=models.CASCADE, verbose_name=_('Organization')
    )
    visited_on = models.DateTimeField(verbose_name=_('Visited on'), auto_now_add=True)


class UserMLData(models.Model):
    """
    ``UserMLData`` is the model representing the attributes that are/can be used to make
    recommendations (of organizations) to a user.

    Attributes:
        user: A ``models.OneToOneField`` field repsenting the user whose
              attributes are been referred to.
        preference_vector: A ``models.BinaryField()`` representing the preference vector of the user.

    """

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, verbose_name=_('User'))
    preference_vector = models.BinaryField()


class UserCoupon(models.Model):
    """
    ``UserCoupon`` is the model representing a coupon associated with a user.
    A user is assigned a coupon upon a successful payment,

    The duplication is required to preserve the details of the coupon, which is otherwise
    prone to updation by the organization owner.

    Attributes:
        title: A ``models.CharField`` representing the title of the coupon.
        description: A ``models.TextField`` representing the description of the coupon.

        organization: A ``models.ForeignKey`` representing the organization associated with the coupon.

        amount: A ``models.PositiveIntegerField`` representing the amount funded.

        validity_start_date: A ``models.DateTimeField`` representing the date and time from which this coupon
                             is valid.
        validity_end_date: A ``models.DateTimeField`` representing the date and time from which this coupon
                           is valid.

        created_at: A ``models.DateTimeField`` representing the date and time when the instance was created.
        updated_at: A ``models.DateTimeField`` representing the date and time when the instaince was updated.

    """

    title = models.CharField(max_length=256, verbose_name=_('Title'))
    description = models.TextField(verbose_name=_('Description'))

    user = models.ForeignKey(
        get_user_model(), related_name='user_coupons',
        on_delete=models.CASCADE, verbose_name=_('User')
    )

    organization = models.ForeignKey(
        Organization, related_name='user_coupons',
        on_delete=models.CASCADE, verbose_name=_('Organization')
    )

    amount = models.PositiveIntegerField(verbose_name=_('Amount'))

    validity_start_date = models.DateTimeField(verbose_name=_('Validity start date'))
    validity_end_date = models.DateTimeField(verbose_name=_('Validity end date'))

    created_at = models.DateTimeField(verbose_name=_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('Updated at'), auto_now=True)
