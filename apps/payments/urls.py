"""
This module provides the URL Configuration for the ``payments`` app.

The ``urlpatterns`` list routes URLs to views. For more information please see:
https://docs.djangoproject.com/en/3.0/topics/http/urls/

"""

from django.urls import path

from apps.payments.views import PaymentAPIView

urlpatterns = [
    path('organization/<int:organization_id>/payment', PaymentAPIView.as_view(), name='payment')
]
