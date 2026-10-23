class CarService():
    def __init__(self, car_repository, state_machine, db_manager):
        self.car_repository = car_repository
        self.state_machine = state_machine
        self.db_manager = db_manager

    def get_all_cars(self, filters):
        return self.car_repository.get_all(filters)

    def get_car_by_id(self, car_id):
        return self.car_repository.get_by_id(car_id)
        
    def create_car(self, car_data):
        return self.state_machine.create("car", car_data)

    def update_car(self, car_id, car_data):
        new_status = car_data.pop("status", None)
        with self.db_manager.transaction():
            car = self.car_repository.get_by_id_for_update(car_id)
            if new_status and new_status != car["status"]:
                self.state_machine.change_status("car", car_id, new_status)

            make_field = "make"
            if make_field not in car_data:
                car_data[make_field] = car[make_field]

            model_field = "model"
            if model_field not in car_data:
                car_data[model_field] = car[model_field]

            year_field = "year"
            if year_field not in car_data:
                car_data[year_field] = car[year_field]
            
            return self.car_repository.update(car_id, car_data)

    def delete_car(self, car_id):
        self.car_repository.delete(car_id)
        return True
