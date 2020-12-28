class TumorValue:
    def __init__(self, db_id, date, value):
        self.db_id = db_id
        self.date = date
        self.value = value

    def __str__(self):
        return f"{self.date.isoformat()} {self.value}"