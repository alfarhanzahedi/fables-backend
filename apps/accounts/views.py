"""
This module provides the different ``view`` classes pertaining to the ``accounts`` app.

"""

from smtplib import SMTPException

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.contrib.auth import get_user_model

import numpy as np
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny

import apps.accounts.constants as constants
from apps.accounts.models import User
from apps.accounts.models import OTP
from apps.accounts.models import UserVisitHistory
from apps.accounts.models import UserMLData
from apps.accounts.models import UserCoupon
from apps.accounts.serializers import EmailSerializer
from apps.accounts.serializers import OTPCodeSerializer
from apps.accounts.serializers import UserSerializer
from apps.accounts.serializers_nested import UserCouponSerializer
from apps.accounts.permissions import UserAPIPermission
from apps.accounts.ml import update_user_preference
from apps.organizations.models import Organization
from apps.organizations.serializers import OrganizationSerializer
from utils.helpers import generate_api_response

class SessionAPIView(APIView):
    """
    ``SessionAPIView`` provides methods to handle the sessions of different users.

    """

    permission_classes = (AllowAny, )

    def post(self, request):
        """
        This method generates an instance of :class:`apps.models.OTP` for the user identified by
        the ``email`` provided in the request body.

        If no such user is present, the user is created first.

        The generated :class:`apps.models.OTP`'s ``code`` is then emailed to the user.

        """

        serializer = EmailSerializer(data=request.data)

        if not serializer.is_valid():
            response = generate_api_response(
                status=settings.API_RESPONSE_STATUS.get('FAIL'),
                data=serializer.errors
            )
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        user = None
        email = serializer.validated_data.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create(
                username=email.split('@')[0],
                email=email,
            )

            preference_vector = np.zeros([99], dtype=np.float32)
            if 'latitude' in request.data and 'longitude' in request.data:
                try:
                    latitude = float(request.data.get('latitude'))
                    longitude = float(request.data.get('longitude'))

                    if constants.MIN_LATITUDE <= latitude <= constants.MAX_LATITUDE and \
                       constants.MIN_LONGITUDE <= latitude <= constants.MAX_LONGITUDE:
                        preference_vector[[0, 1]] = [latitude, longitude]
                except Exception as e:
                    # Ignore if the location data was not provided.
                    pass

            UserMLData.objects.create(
                user=user,
                preference_vector=preference_vector.tobytes()
            )

        OTP.objects.filter(user=user, is_used=False).update(is_used=True)

        otp = OTP.objects.create(user=user)

        try:
            send_mail(
                subject=render_to_string('accounts/otp_code_email_subject.txt'),
                message=render_to_string(
                    'accounts/otp_code_email_plain_text.txt', {
                        'otp': otp
                    }
                ),
                from_email='support@fables.com',
                recipient_list=[user.email],
                html_message=render_to_string(
                    'accounts/otp_code_email.html', {
                        'otp': otp
                    }
                )
            )
        except (ConnectionRefusedError, SMTPException):
            return Response(
                generate_api_response(
                    status=settings.API_RESPONSE_STATUS.get('ERROR'),
                    message='The email can\'t be sent right now. Please try again later. ' +
                    'An internel server error occurred. The operation failed.'
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response(
            generate_api_response(
                status=settings.API_RESPONSE_STATUS.get('SUCCESS')
            ),
            status=status.HTTP_204_NO_CONTENT
        )

    def put(self, request):
        """
        This method verifies the OTP(:class:`apps.models.OTP`) ``code`` provided in the request body, and sets the
        ``auth_token`` cookie.

        If the session token is invalid or expired, appropriate response is returned.

        """

        serializer = OTPCodeSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                generate_api_response(
                    status=settings.API_RESPONSE_STATUS.get('FAIL'),
                    data=serializer.errors
                ),
                status=status.HTTP_400_BAD_REQUEST
            )

        otp = None

        try:
            otp = OTP.objects.select_related('user').get(code__iexact=serializer.validated_data.get('code'))
        except OTP.DoesNotExist:
            return Response(
                generate_api_response(
                    status=settings.API_RESPONSE_STATUS.get('FAIL'),
                    data={
                        'code': ['Invalid OTP code!']
                    }
                ),
                status=status.HTTP_400_BAD_REQUEST
            )

        if otp.is_used:
            return Response(
                generate_api_response(
                    status=settings.API_RESPONSE_STATUS.get('FAIL'),
                    data={
                        'code': ['Used OTP code!']
                    }
                ),
                status=status.HTTP_400_BAD_REQUEST
            )

        if otp.is_expired:
            return Response(
                generate_api_response(
                    status=settings.API_RESPONSE_STATUS.get('FAIL'),
                    data={
                        'code': ['Expired OTP code!']
                    }
                ),
                status=status.HTTP_400_BAD_REQUEST
            )

        if (otp.created_at + timezone.timedelta(minutes=15)) < timezone.now():
            otp.is_expired = True
            otp.save()

            return Response(
                generate_api_response(
                    status=settings.API_RESPONSE_STATUS.get('FAIL'),
                    data={
                        'code': ['Expired OTP code!']
                    }
                ),
                status=status.HTTP_400_BAD_REQUEST
            )

        otp.is_used = True
        otp.save()

        auth_token, _ = Token.objects.get_or_create(user=otp.user)

        return Response(
            generate_api_response(
                status=settings.API_RESPONSE_STATUS.get('SUCCESS'),

                # Seems practical to include the user details in the response
                # upon successful OTP verification.
                data={
                    'user': UserSerializer(otp.user).data,
                    'token': auth_token.key
                }
            ),
            status=status.HTTP_200_OK
        )


class UserAPIView(RetrieveUpdateDestroyAPIView):
    """
    ``UserAPIView`` provides methods to retrieve, update and delete a particular user.

    """

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, UserAPIPermission)

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return Response(
            generate_api_response(
                status=settings.API_RESPONSE_STATUS.get('SUCCESS'),
                data=response.data
            ),
            status=status.HTTP_200_OK
        )

    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        return Response(
            generate_api_response(
                status=settings.API_RESPONSE_STATUS.get('SUCCESS'),
                data=response.data
            ),
            status=status.HTTP_200_OK
        )

    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        return Response(
            generate_api_response(
                status=settings.API_RESPONSE_STATUS.get('SUCCESS'),
                data=response.data
            ),
            status=status.HTTP_200_OK
        )

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        return Response(
            generate_api_response(
                status=settings.API_RESPONSE_STATUS.get('SUCCESS'),
                data=response.data
            ),
            status=status.HTTP_204_NO_CONTENT
        )


class UserVisitHistoryAPIView(APIView):
    """
    ``UserVisitHistoryView`` provides methods to record the visit history (to organizations)
    of a user.

    """

    permission_classes = (IsAuthenticated, )
    def post(self, request, pk):
        """
        This method stores the visit history of a user, and modifies attributes required to generate
        recommendations appropriately.

        """
        if not 'organization_id' in request.data:
            return Response(
                generate_api_response(
                    status=settings.API_RESPONSE_STATUS.get('FAIL'),
                    data='{ "organization_id": "This field is required." }'
                ),
                status=status.HTTP_400_BAD_REQUEST
            )

        visited_organization = None
        visited_organization_id = None

        try:
            visited_organization_id = int(request.data.get('organization_id'))
        except ValueError:
            return Response(
                generate_api_response(
                    status=settings.API_RESPONSE_STATUS.get('FAIL'),
                    data='{ "organization_id": "This field should be an integer." }'
                ),
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            visited_organization = Organization.objects.get(id=visited_organization_id)
        except Organization.DoesNotExist:
            return Response(
                generate_api_response(
                    status=settings.API_RESPONSE_STATUS.get('FAIL'),
                    message=f'No organization exists corresponding to the id - {visited_organization_id}.'
                ),
                status=status.HTTP_400_BAD_REQUEST
            )

        UserVisitHistory.objects.create(user=request.user, organization=visited_organization)

        user_ml_data = None
        try:
            user_ml_data = UserMLData.objects.get(user=request.user)
        except UserMLData.DoesNotExist:
            user_ml_data = UserMLData.objects.create(
                user=request.user,
                preference_vector=np.zeros([99], dtype=np.float32).tobytes()
            )

        updated_preference_vector = update_user_preference(request, user_ml_data, visited_organization_id)

        user_ml_data.preference_vector = updated_preference_vector.tobytes()
        user_ml_data.save()

        return Response(
            generate_api_response(
                status=settings.API_RESPONSE_STATUS.get('SUCCESS'),
                data=None
            ),
            status=status.HTTP_204_NO_CONTENT
        )

class UserCouponAPIView(ListAPIView):
    """
    ``UserCouponAPIView`` provides methods to manipulate coupons issued to a particular
    user.

    """

    serializer_class = UserCouponSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return UserCoupon.objects.filter(user__id=self.kwargs['user_id'])

    def get(self, request, *args, **kwargs):
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


class UserOrganizationAPIView(ListAPIView):
    """
    ``UserOrganizationAPIView`` provides methods to list the organizations owned by a
    particular user.

    """

    serializer_class = OrganizationSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return Organization.objects.filter(owner__id=self.kwargs['user_id'])

    def get(self, request, *args, **kwargs):
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
