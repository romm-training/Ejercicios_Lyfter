class Category_Dto():
    def __init__(self, movement_type, name, color):
        self.movement_type = movement_type
        self.name = name
        self.color = color

    def to_dict(self):
        return {
            "movement_type": self.movement_type,
            "name": self.name,
            "color": self.color
        }

    @classmethod
    def headers(cls):
        return ["movement_type", "name", "color"]


