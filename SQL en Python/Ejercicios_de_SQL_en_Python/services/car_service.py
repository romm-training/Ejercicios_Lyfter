class CarService():
    def __init__(self, car_repository, state_machine, db_manager):
        self.car_repository = car_repository
        self.state_machine = state_machine
        self.db_manager = db_manager

    def get_all_cars(self):
        return self.car_repository.get_all()

    def get_car_by_id(self, car_id):
        return self.car_repository.get_by_id(car_id)
        
    def create_car(self, car_data):
        return self.state_machine.create("car", car_data)

    def update_car(self, car_id, car_data):
        new_status = car_data.pop("status", None)
        with self.db.transaction():
            car = self.car_repository.get_by_id_for_update(car_id)
            if new_status and new_status != car["status"]:
                self.state_machine.change_status("car", car_id, new_status)
            return self.car_repository.update(car_id, car_data)

    def delete_car(self, car_id):
        self.car_repository.delete(car_id)
        return True
