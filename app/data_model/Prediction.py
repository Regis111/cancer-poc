from data_model.TumorValue import TumorValue


class Prediction(TumorValue):
    def __init__(self, db_id, date, value):
        super().__init__(db_id, date, value)
