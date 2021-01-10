"""
This module provides the different ``serializers`` pertaining to the ``organizations`` app.

"""

from rest_framework import serializers

from apps.organizations.models import Organization
from apps.organizations.models import Review
from apps.organizations.models import Coupon
from apps.accounts.serializers import UserSerializer

# Disabling 'abstract-method' warning by pylint for this module.
# pylint: disable=abstract-method

class OrganizationSerializer(serializers.ModelSerializer):
    """
    ``OrganizationSerializer`` is used to serialize an instance of :class:`apps.organizations.models.Organization`.

    """

    owner = UserSerializer(read_only=True)

    class Meta:
        model = Organization
        fields = '__all__'
        read_only_fields = ('id', 'owner', 'created_at', 'updated_at')

class ReviewSerializer(serializers.ModelSerializer):
    """
    ``ReviewSerializer`` is used to serialize an instance of :class:`apps.organizations.models.Review`.

    """

    user = UserSerializer(read_only=True)
    organization = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='organization_detail',
        lookup_url_kwarg='organization_id'
    )

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('id', 'user', 'organization', 'created_at', 'updated_at')


class CouponSerializer(serializers.ModelSerializer):
    """
    ``CouponSerializer`` is used to serialize an instance of :class:`apps.organizations.models.Coupon`.

    """

    def validate(self, attrs):
        """
        This method adds the necessary custom validation to :class:`apps.organizations.serializers.CouponSerializer`.

        """
        if attrs['minimum_fund'] > attrs['maximum_fund']:
            raise serializers.ValidationError({
                'minimum_fund': 'minimum_fund cannot be greater than maximum_fund.'
            })

        if attrs['validity_start_date'] > attrs['validity_end_date']:
            raise serializers.ValidationError({
                'validity_start_date': 'validity_start_date cannot be greater than validity_end_date.'
            })

        organization_id = self.context['view'].kwargs.get('organization_id')

        if Coupon.objects.filter(
                organization__id=organization_id,
                minimum_fund__lte=attrs['maximum_fund'],
                maximum_fund__gte=attrs['minimum_fund']
            ).exists():
            raise serializers.ValidationError({
                'minimum_fund': 'An overlapping fund range already exists.',
                'maximum_fund': 'An overlapping fund range already exists.'
            })

        return attrs

    organization = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='organization_detail',
        lookup_url_kwarg='organization_id'
    )

    class Meta:
        model = Coupon
        fields = '__all__'
        read_only_fields = ('id', 'organization')
