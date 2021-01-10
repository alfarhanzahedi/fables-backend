"""
This module provides the URL Configuration for the ``accounts`` app.

The ``urlpatterns`` list routes URLs to views. For more information please see:
https://docs.djangoproject.com/en/3.0/topics/http/urls/

"""

from django.urls import path

from apps.accounts.views import SessionAPIView
from apps.accounts.views import UserAPIView
from apps.accounts.views import UserVisitHistoryAPIView
from apps.accounts.views import UserCouponAPIView
from apps.accounts.views import UserOrganizationAPIView

urlpatterns = [
    path('session', SessionAPIView.as_view(), name='session'),
    path('user/<int:pk>', UserAPIView.as_view(), name='user'),
    path('user/<int:pk>/visit-history', UserVisitHistoryAPIView.as_view(), name='user_visit_history'),
    path('user/<int:user_id>/coupon', UserCouponAPIView.as_view(), name='user_coupon'),
    path('user/<int:user_id>/organization', UserOrganizationAPIView.as_view(), name='user_organization')
]
