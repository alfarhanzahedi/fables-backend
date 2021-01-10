"""
This module provides the various helper functions that are used by the various
different modules of the project.

"""

from django.utils.crypto import get_random_string

from utils import constants

def generate_api_response(status, data=None, message=None):
    """
    This function adds a wrapper over an API response as per the specification provided
    at https://github.com/omniti-labs/jsend, given the ``status``, the ``data`` and the ``message`` to be returned.

    Args:
        status (str): Any of the response status specified by :const:`notes.settings.base.API_RESPONSE_STATUS`.
        data: The data to be returned by the API call.
        message (str): The message(if any) to be returned by the API call.

    Returns:
        dict: A wrapper over the ``data`` to be returned by the API call.

        The the following ``dict`` is returned:
        ::

            {
                'status': status,
                'data': data,
                'message': message
            }

    """
    response = {}
    response['status'] = status

    if message is None or data is not None:
        response['data'] = data

    if message is not None:
        response['message'] = message

    return response

def get_upload_path(instance, filename):
    """
    This function returns the path where the file is to be uploaded. The filename is replaced
    by a unique string.

    Args:
        instance: The model instance associated with the uploaded file.
        filename (str): The original name of the uploaded file.

    Returns:
        str: The path/location where the file is to be uploaded.

    """
    extension = filename.split('.')[-1]
    return f'{get_random_string(constants.FILENAME_LENGTH)}.{extension}'
