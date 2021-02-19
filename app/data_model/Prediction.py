from data_model.PredictionValue import PredictionValue
from datetime import datetime
from typing import List

from db.config import DATETIME_FORMAT


class Prediction:
    def __init__(
        self,
        db_id: int,
        prediction_values: List[PredictionValue],
        datetime_created: datetime,
        method: str,
        patient_id: int,
    ):
        self.db_id = db_id
        self.prediction_values = prediction_values
        self.datetime_created = datetime_created
        self.method = method
        self.patient_id = patient_id

    def __str__(self):
        return f"{self.db_id} {self.method} {self.datetime_created.strftime(DATETIME_FORMAT)}"
