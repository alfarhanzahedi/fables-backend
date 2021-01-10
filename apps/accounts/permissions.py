"""
This module provides the different permission policies pertaining to the ``accounts`` app.

"""

from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import BasePermission

class SessionAPIPermission(IsAuthenticated):
    """
    ```SessionAPIPermission``` is the permission class used by :ref:``SessionAPIView``.

    The ``DELETE`` request method (i.e. sign-out) is valid only if the user is authenticated!

    """

    def has_permission(self, request, view):
        if request.method in ['POST', 'PUT']:
            return True
        return super().has_permission(request, view)


class UserAPIPermission(BasePermission):
    """
    ```UserAPIPermission``` is the permission class used by :class:`apps.accounts.views.UserAPIView`.

    The permission to retrieve, update, and delete a user should reside with the user itself!

    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user
