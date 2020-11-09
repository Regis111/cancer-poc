class Patient:
    def __init__(self, db_id, name, surname, measurements, predictions):
        self.db_id = db_id
        self.name = name
        self.surname = surname
        self.measurements = measurements
        self.predictions = predictions
