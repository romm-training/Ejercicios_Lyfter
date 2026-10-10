class CarRentalService():
    def __init__(self, car_rental_repository):
        self.car_rental_repository = car_rental_repository

    def get_all_rentals(self):
        try:
            return self.car_rental_repository.get_all()
        except Exception as e:
            print("Error in CarRentalService.get_all_rentals: ", e)
            raise

    def get_rental_by_id(self, rental_id):
        try:
            return self.car_rental_repository.get_by_id(rental_id)
        except Exception as e:
            print("Error in CarRentalService.get_rental_by_id: ", e)
            raise

    def create_rental(self, rental_data):
        try:
            self.car_rental_repository.create(rental_data)
        except Exception as e:
            print("Error in CarRentalService.create_rental: ", e)
            raise

    def update_rental(self, rental_id, rental_data):
        try:
            self.car_rental_repository.update(rental_id, rental_data)
        except Exception as e:
            print("Error in CarRentalService.update_rental: ", e)
            raise

    def delete_rental(self, rental_id):
        try:
            self.car_rental_repository.delete(rental_id)
        except Exception as e:
            print("Error in CarRentalService.delete_rental: ", e)
            raise