"""
  Vectorizer Module: Vectorizes entries for similarity searching
  Classes:
    - Vectorizer

  Author: @captain-pool
"""
import numpy as np
import spacy

class Vectorizer:
  """
    Vectorizer class for vectorizing entries
    Constants needed for scaling raw vectors:
      MAX_LAT: Maximum value of latitude (90)
      MAX_LONG: Maximum value of longitude (180)
      MAX_POSIX: Maximum value of Posix Time (2147483647)
  """
  MAX_LAT = 90
  MAX_LONG = 180
  MAX_POSIX = 2147483647

  def __init__(self, model_name="en_core_web_sm"):
    """
      Args:
        model_name (str): Name of spacy model for vectorizing
                          description. If it doesn't work,
                          please download the spacy model first:
                          `$ python -m spacy download <model_name>`
      Properties:
        dimension [READ ONLY](float32): dimension of each vector.
    """
    self._model = spacy.load(model_name)
    size = self._model("NA").vector.size
    self._vector_dim = size + 3

  @property
  def dimension(self):
    return self._vector_dim

  def vectorize(self, latitude, longitude,
                created_at, description):
    """
      Vectorize each Organization entry
      Args:
        latitude (float32): Latitude of the Organization
        longitude (float32): Longitude of the Organization
        created_at (datetime): datetime object containing
                               date and time of the organzation was registered
        description (string): String description of the organization
      Returns:
        normalized numpy vector of shape, (1, Vectorizer.dimension)
    """
    if not description:
      description = "NA"
    posixtime = created_at.timestamp()
    string_vector = self._model(description).vector

    norm = np.linalg.norm(string_vector)
    string_vector /= norm

    latitude = np.asarray([latitude], dtype=np.float32)
    longitude = np.asarray([longitude], dtype=np.float32)
    posixtime = np.asarray([posixtime], dtype=np.float32)

    final_vector = [
        latitude / Vectorizer.MAX_LAT,
        longitude / Vectorizer.MAX_LONG,
        posixtime / Vectorizer.MAX_POSIX,
        string_vector]

    return np.concatenate(final_vector)[np.newaxis, :]
