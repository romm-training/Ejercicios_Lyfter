class CarService():
    def __init__(self, car_repository, state_machine):
        self.car_repository = car_repository
        self.state_machine = state_machine

    def get_all_cars(self):
        try:
            return self.car_repository.get_all()
        except Exception as e:
            print("Error in CarService.get_all_cars: ", e)
            raise

    def get_car_by_id(self, car_id):
        try:
            return self.car_repository.get_by_id(car_id)
        except Exception as e:
            print("Error in CarService.get_car_by_id: ", e)
            raise

    def create_car(self, car_data):
        try:
            #self.car_repository.create(car_data)
            return self.state_machine.create("car", car_data)
        except Exception as e:
            print("Error in CarService.create_car: ", e)
            raise

    def update_car(self, car_id, car_data):
        try:
            return self.state_machine.update(car_id, car_data)
        except Exception as e:
            print("Error in CarService.update_car: ", e)
            raise

    def delete_car(self, car_id):
        try:
            self.car_repository.delete(car_id)
            return True
        except Exception as e:
            print("Error in CarService.delete_car: ", e)
            raise