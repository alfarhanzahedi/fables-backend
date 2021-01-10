"""
This module provides the different ``models`` pertaining to the ``organizations`` app.

"""


from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator

import apps.organizations.constants as constants

class Organization(models.Model):
    """
    ``Organization`` is the model representing an organization in need of funds.

    Attributes:
        name: A ``models.CharField()`` representing the name of the organization.
        description: A ``models.TextField()`` representing a description of the organization.

        owner: A ``models.ForeignKey()`` field representing the owner of the orgnaization.

        email: A ``models.EmailField()`` representing the email of the organization.

        address: A ``models.CharField()`` representing the address of the organization.
        latitute: A ``models.FloatField()`` representing the geographical latitude on which the organization is located.
        longitude: A ``models.FloatField()`` representing the geogpraghical longitude on which
                   the organization is located.

        created_at: A ``models.DateTimeField()`` representing the date and time when the instance was created.
        updated_at: A ``models.DateTimeField()`` representing the date and time when the instaince was updated.

    """

    name = models.CharField(verbose_name=_('Name'), max_length=256)
    description = models.TextField(verbose_name=_('Description'))

    owner = models.ForeignKey(
        get_user_model(), related_name='organizations',
        on_delete=models.CASCADE, verbose_name=_('Owner')
    )

    email = models.EmailField(verbose_name=_('Email'))

    amount_to_be_raised = models.PositiveIntegerField(
        verbose_name=_('Amount to be raised?')
    )

    address = models.CharField(verbose_name=_('Address'), max_length=1024)
    latitude = models.FloatField(verbose_name=_('Latitude'))
    longitude = models.FloatField(verbose_name=_('Longitude'))

    created_at = models.DateTimeField(verbose_name=_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('Updated at'), auto_now=True)


class Review(models.Model):
    """
    ``Review`` is the model representing a review for an organization.

    Attributes:
        rating: A ``models.SmallIntegerField()`` representing the rating given to an organization (out of 5).
        comment: A ``models.TextField()`` representing the comment/review given to an organization.

        user: A ``models.ForeignKey()`` field representing the user who gave the rating and/or the comment.
        organization: A ``models.ForiegnKey()`` field representing the origanization to which the user
                      has given the rating and/or comment.

        created_at: A ``models.DateTimeField()`` representing the date and time when the instance was created.
        updated_at: A ``models.DateTimeField()`` representing the date and time when the instaince was updated.

    """

    rating = models.SmallIntegerField(
        verbose_name=_('Rating'), default=constants.REVIEW_MAX_RATING,
        validators=[
            MaxValueValidator(constants.REVIEW_MAX_RATING),
            MinValueValidator(constants.REVIEW_MIN_RATING)
        ]
    )
    comment = models.TextField(verbose_name=_('Comment'), null=True, blank=True)

    user = models.ForeignKey(
        get_user_model(), related_name='reviews',
        on_delete=models.CASCADE, verbose_name=_('User')
    )
    organization = models.ForeignKey(
        Organization, related_name='reviews',
        on_delete=models.CASCADE, verbose_name=_('Organization')
    )

    created_at = models.DateTimeField(verbose_name=_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('Updated at'), auto_now=True)

class Coupon(models.Model):
    """
    ``Coupon`` is the model representing a coupon associated with an organization.

    Attributes:
        title: A ``models.CharField`` representing the title of the coupon.
        description: A ``models.TextField`` representing the description of the coupon.

        organization: A ``models.ForeignKey`` representing the organization associated with the coupon.

        minimum_fund: A ``models.PositiveIntegerField`` representing the minimum fund on which this coupon
                      is to be issued.
        maximum_fund: A ``models.PositiveIntegerField`` representing the maximum fund on which this coupon
                      is to be issued.

        validity_start_date: A ``models.DateTimeField`` representing the date and time from which this coupon
                             is valid.
        validity_end_date: A ``models.DateTimeField`` representing the date and time from which this coupon
                           is valid.

        created_at: A ``models.DateTimeField`` representing the date and time when the instance was created.
        updated_at: A ``models.DateTimeField`` representing the date and time when the instaince was updated.

    """

    title = models.CharField(max_length=256, verbose_name=_('Title'))
    description = models.TextField(verbose_name=_('Description'))

    organization = models.ForeignKey(
        Organization, related_name='coupons',
        on_delete=models.CASCADE, verbose_name=_('Organization')
    )

    minimum_fund = models.PositiveIntegerField(verbose_name=_('Minimum fund'))
    maximum_fund = models.PositiveIntegerField(verbose_name=_('Maximum fund'))

    validity_start_date = models.DateTimeField(verbose_name=_('Validity start date'))
    validity_end_date = models.DateTimeField(verbose_name=_('Validity end date'))

    created_at = models.DateTimeField(verbose_name=_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('Updated at'), auto_now=True)
