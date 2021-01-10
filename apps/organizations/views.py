"""
This module provides the different ``view`` classes pertaining to the ``organizations`` app.

"""

from django.conf import settings
from django.http import Http404
from django.db.models import Sum

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from apps.organizations.models import Organization
from apps.organizations.models import Review
from apps.organizations.models import Coupon
from apps.organizations.serializers import OrganizationSerializer
from apps.organizations.serializers import ReviewSerializer
from apps.organizations.serializers import CouponSerializer
from apps.organizations.permissions import OrganizationAPIPermission
from apps.organizations.permissions import ReviewAPIPermission
from apps.organizations.permissions import CouponAPIPermission
from apps.organizations.ml import insert_semantic_vector
from apps.organizations.ml import get_recommendations
from apps.payments.models import Payment
from utils.helpers import generate_api_response

class OrganizationAPIView(ListCreateAPIView):
    """
    ``OrganizationAPIView`` provides methods to list and create organizations.

    """

    queryset = Organization.objects.all().select_related('owner')
    serializer_class = OrganizationSerializer
    permission_classes = (OrganizationAPIPermission, )

    def get(self, request, *args, **kwargs):
        """
        List all organizations.

        """
        response = None
        if request.user.is_authenticated:

            recommended_organization_ids = get_recommendations(
                user=request.user,
                number_of_recommendations=100
            )
            serializer = OrganizationSerializer(
                Organization.objects.filter(id__in=recommended_organization_ids),
                many=True
            )
            response = Response(serializer.data, status=status.HTTP_200_OK)
        else:
            response = super().get(request, *args, **kwargs)
        return Response(
            generate_api_response(
                status=settings.API_RESPONSE_STATUS.get('SUCCESS'),
                data={
                    'organizations': response.data
                }
            ),
            status=response.status_code
        )

    def post(self, request, *args, **kwargs):
        """
        Create an organization.

        """
        response = super().post(request, *args, **kwargs)
        organization = Organization.objects.get(id=response.data.get('id'))

        insert_semantic_vector(organization)

        return Response(
            generate_api_response(
                status=settings.API_RESPONSE_STATUS.get('SUCCESS'),
                data={
                    'organization': response.data
                }
            ),
            status=response.status_code
        )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class OrganizationDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    ``OrganizationDetailAPIView`` provides methods to retrieve, update and delete an organization.

    """

    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = (OrganizationAPIPermission, )
    lookup_url_kwarg = 'organization_id'
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        # Compute and add the amount raised by the organization to the response.
        amount_raised = Payment.objects.filter(
            organization__id=self.kwargs['organization_id']
        ).aggregate(
            Sum('amount')
        )
        response.data.update({'amount_raised': amount_raised['amount__sum']})

        return Response(
            generate_api_response(
                status=settings.API_RESPONSE_STATUS.get('SUCCESS'),
                data={
                    'organization': response.data
                }
            ),
            status=response.status_code
        )

    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        return Response(
            generate_api_response(
                status=settings.API_RESPONSE_STATUS.get('SUCCESS'),
                data={
                    'organization': response.data
                }
            ),
            status=response.status_code
        )

    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        return Response(
            generate_api_response(
                status=settings.API_RESPONSE_STATUS.get('SUCCESS'),
                data={
                    'organization': response.data
                }
            ),
            status=response.status_code
        )

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        return Response(
            generate_api_response(
                status=settings.API_RESPONSE_STATUS.get('SUCCESS'),
                data=response.data
            ),
            status=response.status_code
        )

class ReviewAPIView(ListCreateAPIView):
    """
    ``ReviewAPIView`` provides methods to list and create reviews of an organization.

    """

    serializer_class = ReviewSerializer
    permission_classes = (ReviewAPIPermission, )

    def get_queryset(self):
        return Review.objects.filter(organization__id=self.kwargs['organization_id']).select_related('user')

    def get(self, request, *args, **kwargs):
        try:
            Organization.objects.get(id=self.kwargs['organization_id'])
        except Organization.DoesNotExist:
            return Response(
                generate_api_response(
                    status=settings.API_RESPONSE_STATUS.get('FAIL'),
                    data=f'No organization exists corresponding to the id - {self.kwargs["organization_id"]}.'
                ),
                status=status.HTTP_404_NOT_FOUND
            )

        response = super().get(request, *args, **kwargs)

        return Response(
            generate_api_response(
                status=settings.API_RESPONSE_STATUS.get('SUCCESS'),
                data={
                    'reviews': response.data
                }
            ),
            status=response.status_code
        )

    def post(self, request, *args, **kwargs):
        try:
            Organization.objects.get(id=self.kwargs['organization_id'])
        except Organization.DoesNotExist:
            return Response(
                generate_api_response(
                    status=settings.API_RESPONSE_STATUS.get('FAIL'),
                    data=f'No organization exists corresponding to the id - {self.kwargs["organization_id"]}.'
                ),
                status=status.HTTP_404_NOT_FOUND
            )

        response = super().post(request, *args, **kwargs)

        return Response(
            generate_api_response(
                status=settings.API_RESPONSE_STATUS.get('SUCCESS'),
                data={
                    'review': response.data
                }
            ),
            status=response.status_code
        )

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            organization=Organization.objects.get(id=self.kwargs['organization_id'])
        )

class ReviewDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    ``ReviewDetailAPIView`` provides methods to retrieve, update and delete a review of an organization.

    """

    serializer_class = ReviewSerializer
    permission_classes = (ReviewAPIPermission, )
    lookup_url_kwarg = 'review_id'
    lookup_field = 'pk'

    def get_queryset(self):
        return Review.objects.filter(organization__id=self.kwargs['organization_id'])

    def handle_exception(self, exc):
        if isinstance(exc, Http404):
            return Response(
                generate_api_response(
                    status=settings.API_RESPONSE_STATUS.get('FAIL'),
                    data=f'No review, with id - {self.kwargs["review_id"]}, exists for the organization ' +
                    f'identified by id - {self.kwargs["organization_id"]}.'
                ),
                status=status.HTTP_404_NOT_FOUND
            )

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return Response(
            generate_api_response(
                status=settings.API_RESPONSE_STATUS.get('SUCCESS'),
                data={
                    'review': response.data
                }
            ),
            status=response.status_code
        )

    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        return Response(
            generate_api_response(
                status=settings.API_RESPONSE_STATUS.get('SUCCESS'),
                data={
                    'review': response.data
                }
            ),
            status=response.status_code
        )

    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        return Response(
            generate_api_response(
                status=settings.API_RESPONSE_STATUS.get('SUCCESS'),
                data={
                    'review': response.data
                }
            ),
            status=response.status_code
        )

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        return Response(
            generate_api_response(
                status=settings.API_RESPONSE_STATUS.get('SUCCESS'),
                data=response.data
            ),
            status=response.status_code
        )


class CouponAPIView(ListCreateAPIView):
    """
    ``CouponAIView`` provides methods to list and create coupons for an organization.

    """

    serializer_class = CouponSerializer
    permission_classes = (CouponAPIPermission, )

    def get_queryset(self):
        return Coupon.objects.filter(organization__id=self.kwargs['organization_id']) \
                             .select_related('organization__owner')

    def get(self, request, *args, **kwargs):
        try:
            Organization.objects.get(id=self.kwargs['organization_id'])
        except Organization.DoesNotExist:
            return Response(
                generate_api_response(
                    status=settings.API_RESPONSE_STATUS.get('FAIL'),
                    data=f'No organization exists corresponding to the id - {self.kwargs["organization_id"]}.'
                ),
                status=status.HTTP_404_NOT_FOUND
            )

        response = super().get(request, *args, **kwargs)

        return Response(
            generate_api_response(
                status=settings.API_RESPONSE_STATUS.get('SUCCESS'),
                data={
                    'coupons': response.data
                }
            ),
            status=response.status_code
        )

    def post(self, request, *args, **kwargs):
        try:
            Organization.objects.get(id=self.kwargs['organization_id'], owner=request.user)
        except Organization.DoesNotExist:
            return Response(
                generate_api_response(
                    status=settings.API_RESPONSE_STATUS.get('FAIL'),
                    data=f'No organization exists corresponding to the id - {self.kwargs["organization_id"]}, ' +
                    f'and with owner(user) corresponding to the id - {request.user.id}.'
                ),
                status=status.HTTP_404_NOT_FOUND
            )

        response = super().post(request, *args, **kwargs)

        return Response(
            generate_api_response(
                status=settings.API_RESPONSE_STATUS.get('SUCCESS'),
                data={
                    'coupon': response.data
                }
            ),
            status=response.status_code
        )

    def perform_create(self, serializer):
        serializer.save(
            organization=Organization.objects.get(id=self.kwargs['organization_id'])
        )


class CouponDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    ``CouponDetailAPIView`` provides methods to retrieve, update and delete a coupon of an organization.

    """

    serializer_class = CouponSerializer
    permission_classes = (CouponAPIPermission, )
    lookup_url_kwarg = 'coupon_id'
    lookup_field = 'pk'

    def get_queryset(self):
        return Coupon.objects.filter(organization__id=self.kwargs['organization_id']) \
                             .select_related('organization__owner')

    def handle_exception(self, exc):
        if isinstance(exc, Http404):
            return Response(
                generate_api_response(
                    status=settings.API_RESPONSE_STATUS.get('FAIL'),
                    data=f'No coupon, with id - {self.kwargs["coupon_id"]}, exists for the organization ' +
                    f'identified by id - {self.kwargs["organization_id"]}.'
                ),
                status=status.HTTP_404_NOT_FOUND
            )

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return Response(
            generate_api_response(
                status=settings.API_RESPONSE_STATUS.get('SUCCESS'),
                data={
                    'coupon': response.data
                }
            ),
            status=response.status_code
        )

    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        return Response(
            generate_api_response(
                status=settings.API_RESPONSE_STATUS.get('SUCCESS'),
                data={
                    'coupon': response.data
                }
            ),
            status=response.status_code
        )

    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        return Response(
            generate_api_response(
                status=settings.API_RESPONSE_STATUS.get('SUCCESS'),
                data={
                    'coupon': response.data
                }
            ),
            status=response.status_code
        )

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        return Response(
            generate_api_response(
                status=settings.API_RESPONSE_STATUS.get('SUCCESS'),
                data=response.data
            ),
            status=response.status_code
        )
