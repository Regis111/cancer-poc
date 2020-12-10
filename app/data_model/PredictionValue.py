from datetime import date

from data_model.TumorValue import TumorValue


class PredictionValue(TumorValue):
    """For creation please us functions from db module instead of Python object creation"""

    def __init__(self, db_id: int, prediction_date: date, value: float):
        super().__init__(db_id, prediction_date, value)
