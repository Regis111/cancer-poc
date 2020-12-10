from data_model.Measurement import Measurement
from data_model.PredictionValue import PredictionValue

from typing import List, Dict
from datetime import datetime


class Patient:
    """For creation please us functions from db module instead of Python object creation"""

    def __init__(
        self,
        db_id: int,
        name: str,
        surname: str,
        measurements: List[Measurement],
        predictions: Dict[datetime, List[PredictionValue]],
    ):
        self.db_id = db_id
        self.name = name
        self.surname = surname
        self.measurements = measurements
        self.predictions = predictions

    def __str__(self):
        return f"{self.name} {self.surname}"
