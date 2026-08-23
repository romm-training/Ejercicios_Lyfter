from dto import movement_dto
from persistency import persistency_movement

class Movement_Biz():
    def add_data(movement_dto):
        persistency_movement.append_data(movement_dto)

    def read_data() -> list:
        data = []
        try:
            data = persistency_movement.read_data()
        except FileNotFoundError as e:
            print(f"Error: {e}")
        return data