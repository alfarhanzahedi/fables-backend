"""
This module provides the different permission policies pertaining to the ``organizations`` app.

"""

from rest_framework.permissions import IsAuthenticated

class OrganizationAPIPermission(IsAuthenticated):
    """
    ```OrganizationAPIPermission``` is the permission class used by
    :class:`apps.organizations.views.OrganizationAPIView` and
    :class:`apps.organizations.views.OrganizationDetailAPIView`.

    The permission to update and delete an organization should reside with the owner of the organization itself!

    """

    def has_permission(self, request, view):
        if request.method in ['GET']:
            return True

        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET']:
            return True

        return obj.owner == request.user

class ReviewAPIPermission(IsAuthenticated):
    """
    ```ReviewAPIPermission``` is the permission class used by
    :class:`apps.organizations.views.ReviewAPIView` and
    :class:`apps.organizations.views.ReviewDetailAPIView`.

    The permission to update and delete a review should reside with the user who made the review!

    """

    def has_permission(self, request, view):
        if request.method in ['GET']:
            return True

        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET']:
            return True

        return obj.user == request.user

class CouponAPIPermission(IsAuthenticated):
    """
    ``CouponAPIPermission`` is the permission calss used by
    :class:`apps.organizations.views.CouponAPIView` and
    :class:`apps.organizations.views.CouponAPIDetailView`.

    The permission to update and delete a coupon should reside with the organization's owner!

    """

    def has_permission(self, request, view):
        if request.method in ['GET']:
            return True

        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET']:
            return True

        return obj.organization.owner == request.user
