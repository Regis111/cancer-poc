from data_model.TumorValue import TumorValue


class Measurement(TumorValue):
    """For creation please us functions from db module instead of Python object creation"""

    def __init__(self, db_id, date, value):
        super().__init__(db_id, date, value)

    def __str__(self):
        return f"Pomiar {self.date} {self.value}"
