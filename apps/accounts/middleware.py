"""
This module provides the different middlewares pertaining to the ``accounts`` app.

"""

from secrets import token_hex

import apps.accounts.constants as constants

class CSRFMiddleware:
    """
    CSRFMiddleWare adds a random :const:`apps.accounts.constants.CSRF_TOKEN_LENGTH` character
    ``csrf_token`` token to the response.

    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "DELETE, GET, OPTIONS, PATCH, POST, PUT"	
        response["Access-Control-Allow-Headers"] = "accept, accept-encoding, authorization, content-type, dnt, origin, user-agent, x-csrftoken, x-requested-with"
        response.set_cookie(
            'csrf_token',
            token_hex(constants.CSRF_TOKEN_LENGTH),
            samesite='strict'
        )
        return response
