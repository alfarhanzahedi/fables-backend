"""
This module contains all things ML for the app - ``organizations``.
Why a different module? To protect the code with ``pyarmour`` :D

"""

import numpy as np

from django.conf import settings

import mldb.database
import mldb.vectorizer
from apps.accounts.models import UserMLData

def insert_semantic_vector(organization):
    """
    This function inserts the semantic vector (of an organization) into the DB.

    """
    vector = mldb.vectorizer.Vectorizer()
    db = mldb.database.Database(settings.MLDB_DB_PATH, vector.dimension)

    semantic_vector = vector.vectorize(
        organization.latitude, organization.longitude, organization.created_at, organization.description
    ).astype('float32')

    db.open()
    db.insert(organization.id, semantic_vector)
    db.write()

def get_recommendations(user, number_of_recommendations):
    """
    This function returns the ids of the recommended organizations for a particular user.

    """
    user_ml_data = UserMLData.objects.get(user=user)
    preference_vector = np.fromstring(user_ml_data.preference_vector, dtype=np.float32)

    vector = mldb.vectorizer.Vectorizer()
    db = mldb.database.Database(settings.MLDB_DB_PATH, vector.dimension)
    db.open()

    return db.nearest(preference_vector, num_closest=number_of_recommendations)
