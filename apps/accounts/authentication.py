"""
This module provides the different authentication policies that can be used in place of the ones
provided by Django and DRF.

"""

from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions

class TokenAuthenticationCookieSupport(TokenAuthentication):
    """
    ``TokenAuthenticationCookieSupport`` extends DRF's
    ``TokenAuthentication`` class to support cookie based token authentication, along with using
    **Double Submit Cookie Pattern** to prevent CSRF attacks.

    Upon authentication, the token associated with the user/account is set as an ``httpOnly``
    cookie with the name being ``auth_token``.

    The **Double Submit Cookie Pattern** is implemented as follows:

    - The server sets a ``csrf_token`` cookie with every response.

    - On each request (if ``auth_token`` cookie is set), the server checks
      if the ``csrf_token`` matches with ``HTTP_CSRF_TOKEN`` in the request header.

      The client is supposed to read the ``csrf_token`` cookie from the response and
      set it in a custom header - ``HTTP_CSRF_TOKEN`` for the next request.

    """

    def authenticate(self, request):
        """
        This method implements the **Double Submit Cookie Pattern** as described above.

        Returns:
            ``None``, if ``auth_token`` cookie is not set.

            After performing the necessary checks as per the **Double Submit Cookie Pattern**
            (described above), this method calls :func:`authenticate_credentials`, and returns
            the result of the method call.

        Raises:
            PermissionDenied:
                - If ``HTTP_CSRF_TOKEN`` is not present in the request header.
                - If ``csrf_token`` cookie is absent.
                - If ``HTTP_CSRF_TOKEN`` is not equal to ``csrf_token``.

        """
        if not 'auth_token' in request.COOKIES:
            return None

        if not 'HTTP_CSRF_TOKEN' in request.META:
            raise exceptions.PermissionDenied('"CSRF-TOKEN" missing in request header.')

        if not 'csrf_token' in request.COOKIES:
            raise exceptions.PermissionDenied('"csrf_token" missing in cookies.')

        if not request.COOKIES.get('csrf_token') == request.META.get('HTTP_CSRF_TOKEN'):
            raise exceptions.PermissionDenied(
                '"CSRF-TOKEN" in request header does not match with "csrf_token" in cookies.'
            )

        return self.authenticate_credentials(
            request.COOKIES.get('auth_token')
        )

    def authenticate_credentials(self, key):
        """
        This method returns a ``(user, token)`` tuple if a user corresponding to the token
        specified by ``key`` exists in the database.

        Args:
            key (str): The string identifying the authentication token.

        Returns:
            A tuple - ``(user, token)``, where ``user`` is the user to which the ``token`` belongs.

        Raises:
            AuthenticationFailed:
                If a user corresponding to the token specified by ``key`` exists in the database, or
                if the user account is **inactive** or was **deleted**.

        """
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key__iexact=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid authentication token.')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted.')

        return (token.user, token)
