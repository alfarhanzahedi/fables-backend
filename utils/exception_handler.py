"""
This module provides the exception handler that can be used in place of the
default exception handler provided by DRF.

"""

from django.conf import settings

from rest_framework.views import exception_handler as rest_framework_exception_handler

from utils.helpers import generate_api_response

def exception_handler(exception, context):
    """
    This function returns the response that should be used for any given exception.

    It calls the DRF's exception handler -
    ``rest_framework.views.exception_handler(exception, context)``
    first, modifies the response thus obtained by adding a wrapper over it, and then
    returns it.

    Why modify the response?
    See the specification provided here: https://github.com/omniti-labs/jsend

    """
    response = rest_framework_exception_handler(exception, context)

    # rest_framework_exception_handler may return `None` in cases where exception cannot be handled.
    # In such cases, the best course of action would be to return `None` as it will cause a
    # 500 error to be raised.
    if response is not None:
        response.data = generate_api_response(
            status=settings.API_RESPONSE_STATUS.get('FAIL'),
            data=response.data['detail'] if 'detail' in response.data else response.data
        )

    return response
