"""
This module provides the different ``view`` classes pertaining to the ``payments`` app.

"""

from django.conf import settings

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from apps.accounts.models import UserCoupon
from apps.organizations.models import Organization
from apps.organizations.models import Coupon
from apps.payments.models import Payment
from apps.payments.serializers import PaymentSerializer
from utils.helpers import generate_api_response

class PaymentAPIView(APIView):
    """
    ``PaymentAPIView`` handles all the functionalities pertaining to the payments made
    in the application.

    """

    permission_classes = (IsAuthenticated, )

    def post(self, request, organization_id):
        """
        This method checks if the payment is valid or not and stores the relevant information
        in the database.

        """

        organization = None
        try:
            organization = Organization.objects.get(id=organization_id)
        except Organization.DoesNotExist:
            return Response(
                generate_api_response(
                    status=settings.API_RESPONSE_STATUS.get('FAIL'),
                    data=f'No organization exists corresponding to the id - {organization_id}.'
                ),
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = PaymentSerializer(data=request.data)

        if not serializer.is_valid():
            response = generate_api_response(
                status=settings.API_RESPONSE_STATUS.get('FAIL'),
                data=serializer.errors
            )
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        amount = serializer.validated_data.get('amount')

        approprite_coupon = Coupon.objects.filter(
            organization__id=organization_id,
            minimum_fund__lte=amount,
            maximum_fund__gte=amount
        ).first()

        # If no coupon is present, do not issue any coupons.
        # Just accept the payments as donation.
        if approprite_coupon is None:
            Payment.objects.create(
                user=request.user,
                organization=organization,
                amount=amount
            )

            return Response(
                generate_api_response(
                    status=settings.API_RESPONSE_STATUS.get('SUCCESS'),
                    data=None
                ),
                status=status.HTTP_204_NO_CONTENT
            )

        # Assign a coupon to the user if coupon is present.
        user_coupon = UserCoupon.objects.create(
            title=approprite_coupon.title,
            description=approprite_coupon.description,
            organization=organization,
            user=request.user,
            amount=amount,
            validity_start_date=approprite_coupon.validity_start_date,
            validity_end_date=approprite_coupon.validity_end_date
        )

        # Store the details of the payment
        Payment.objects.create(
            user=request.user,
            organization=organization,
            amount=amount,
            user_coupon=user_coupon
        )

        return Response(
            generate_api_response(
                status=settings.API_RESPONSE_STATUS.get('SUCCESS'),
                data=None
            ),
            status=status.HTTP_204_NO_CONTENT
        )
