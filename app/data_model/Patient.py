from data_model.Prediction import Prediction
from data_model.Measurement import Measurement
from data_model.Treatment import Treatment

from typing import List


class Patient:
    """For creation please us functions from db module instead of Python object creation"""

    def __init__(
        self,
        db_id: int,
        name: str,
        surname: str,
        measurements: List[Measurement],
        predictions: List[Prediction],
        treatments: List[Treatment],
    ):
        self.db_id = db_id
        self.name = name
        self.surname = surname
        self.measurements = measurements
        self.predictions = predictions
        self.treatments = treatments

    def __str__(self):
        return f"{self.name} {self.surname}"
