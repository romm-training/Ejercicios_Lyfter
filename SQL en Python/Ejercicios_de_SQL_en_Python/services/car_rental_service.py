class CarRentalService():
    def __init__(self, car_rental_repository, state_machine, db_manager):
        self.car_rental_repository = car_rental_repository
        self.state_machine = state_machine
        self.db_manager = db_manager

    def get_all_rentals(self, filters):
        return self.car_rental_repository.get_all(filters)

    def get_rental_by_id(self, rental_id):
        return self.car_rental_repository.get_by_id(rental_id)

    def create_rental(self, rental_data):
        return self.state_machine.create("car_rental", rental_data)

    def update_rental(self, rental_id, rental_data):
        new_status = rental_data.pop("status", None)
        with self.db_manager.transaction():
            rental = self.car_rental_repository.get_by_id_for_update(rental_id)
            if new_status and new_status != rental["status"]:
                self.state_machine.change_status("car_rental", rental_id, new_status)

            return_date_field_name = "return_date_at"
            if return_date_field_name not in rental_data:
                rental_data[return_date_field_name] = rental[return_date_field_name]

            return self.car_rental_repository.update(rental_id, rental_data)

    def delete_rental(self, rental_id):
        self.car_rental_repository.delete(rental_id)
        return True
