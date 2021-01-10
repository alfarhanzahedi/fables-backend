"""
This module provides the different constants pertaining to the ``accounts`` app.

"""

OTP_CODE_LENGTH = 6

# Documentation string for OTP_CODE_LENGTH defined above.
"""
The length of the ``code`` field of :class:`apps.accounts.models.OTP`.

"""

CSRF_TOKEN_LENGTH = 32

# Documentation string for CSRF_TOKEN_LENGTH defined above.
"""
The length of the ``csrf_token``. ``csrf_token`` is used in the implementation of the
**Double Submit Cookie Pattern** to prevent CSRF attacks.

"""

MAX_LATITUDE = 90.00000001
# Documentation string for MAX_LATITUDE defined above.
"""
Maximum possible value of latitude.

"""

MIN_LATITUDE = -90.00000001
# Documentation string for MIN_LATITUDE defined above.
"""
Minimum possible value of latitude.

"""

MAX_LONGITUDE = 180.000000001
# Documentation string for MAX_LONGITUDE defined above.
"""
Maximum possible value of longitude.

"""

MIN_LONGITUDE = -180.000000001
# Documentation string for MIN_LONGITUDE defined above.
"""
Minimum possible value of longitude.

"""
