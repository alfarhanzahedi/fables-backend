"""
This module provides the URL Configuration for the ``organizations`` app.

The ``urlpatterns`` list routes URLs to views. For more information please see:
https://docs.djangoproject.com/en/3.0/topics/http/urls/

"""

from django.urls import path

from apps.organizations.views import OrganizationAPIView
from apps.organizations.views import OrganizationDetailAPIView
from apps.organizations.views import ReviewAPIView
from apps.organizations.views import ReviewDetailAPIView
from apps.organizations.views import CouponAPIView
from apps.organizations.views import CouponDetailAPIView

urlpatterns = [
    path('organization', OrganizationAPIView.as_view(), name='organization'),
    path('organization/<int:organization_id>', OrganizationDetailAPIView.as_view(), name='organization_detail'),
    path('organization/<int:organization_id>/review', ReviewAPIView.as_view(), name='review'),
    path(
        'organization/<int:organization_id>/review/<int:review_id>',
        ReviewDetailAPIView.as_view(),
        name='review_detail'
    ),
    path('organization/<int:organization_id>/coupon', CouponAPIView.as_view(), name='coupon'),
    path(
        'organization/<int:organization_id>/coupon/<int:coupon_id>',
        CouponDetailAPIView.as_view(),
        name='coupon_detail'
    )
]
