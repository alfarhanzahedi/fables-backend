"""
This module contains all things ML for the app - ``account``.
Why a different module? To protect the code with ``pyarmour`` :D

"""

import numpy as np

from django.conf import settings

import mldb.database
import mldb.vectorizer
import apps.accounts.constants as constants
from apps.accounts.models import UserVisitHistory

def update_user_preference(request, user_ml_data, visited_organization_id):
    """
    This function updates the preference vector provided in the parameter - ``user_ml_data``.

    """

    preference_vector = np.fromstring(user_ml_data.preference_vector, dtype=np.float32)

    vector = mldb.vectorizer.Vectorizer()
    db = mldb.database.Database(settings.MLDB_DB_PATH, vector.dimension)
    db.open()

    organization_vector = db.search_vector(visited_organization_id)

    if 'latitude' in request.data and 'longitude' in request.data:
        try:
            latitude = float(request.data.get('latitude'))
            longitude = float(request.data.get('longitude'))

            if constants.MIN_LATITUDE <= latitude <= constants.MAX_LATITUDE and \
                constants.MIN_LONGITUDE <= latitude <= constants.MAX_LONGITUDE:
                preference_vector[[0, 1]] = [
                    latitude / mldb.vectorizer.Vectorizer.MAX_LAT,
                    longitude / mldb.vectorizer.Vectorizer.MAX_LONG
                ]
        except Exception as e:
            # Ignore if the location data was not provided.
            pass

    preference_vector[2: ] += organization_vector[2: ]

    organization_count = UserVisitHistory.objects.filter(user=request.user).count()

    preference_vector[2: ] /= organization_count

    return preference_vector
