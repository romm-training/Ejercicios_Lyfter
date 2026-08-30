class Movement_Dto():
    def __init__(self, date, type, category, description, amount):
        self.date = date
        self.type = type
        self.category = category
        self.description = description
        self.amount = amount

    def to_dict(self):
        return {
            "date": self.date,
            "type": self.type,
            "category": self.category,
            "description": self.description,
            "amount": self.amount
        }

    @classmethod
    def headers(cls):
        return ["date","type","category","description","amount"]
