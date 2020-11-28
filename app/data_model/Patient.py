class Patient:
    """For creation please us functions from db module instead of Python object creation"""

    def __init__(self, db_id, name, surname, measurements, predictions):
        self.db_id = db_id
        self.name = name
        self.surname = surname
        self.measurements = measurements
        self.predictions = predictions

    def __str__(self):
        return f"{self.name} {self.surname}"
