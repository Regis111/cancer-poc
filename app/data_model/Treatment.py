class Treatment:
    def __init__(self, db_id, date, amount):
        self.db_id = db_id
        self.date = date
        self.amount = amount

    def __str__(self):
        return f"{self.date.isoformat()}"
