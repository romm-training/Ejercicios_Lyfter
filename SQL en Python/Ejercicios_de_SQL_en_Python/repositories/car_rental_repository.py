class CarRentalRepository():
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def _format_record(self, car_rental_record):
        return {
            "id": car_rental_record[0],
            "user_id": car_rental_record[1],
            "car_id": car_rental_record[2],
            "rental_date_at": car_rental_record[3],
            "return_date_at": car_rental_record[4],
            "status": car_rental_record[5]
        }

    def get_all(self):
        try:
            results = self.db_manager.execute_query(
                "SELECT id, user_id, car_id, rental_date_at, return_date_at, status " \
                "FROM lyfter_car_rental.car_rental;"
            )
            formatted_results = [self._format_record(result) for result in results]
            print("Retrieved all car rentals from database.")
            return formatted_results
        except Exception as e:
            print("Error getting all car rentals from database: ", e)
            raise

    def get_by_id(self, rental_id):
        try:
            results = self.db_manager.execute_query(
                "SELECT id, user_id, car_id, rental_date_at, return_date_at, status " \
                "FROM lyfter_car_rental.car_rental " \
                "WHERE id = %s;",
                (rental_id,)
            )
            formatted_results = self._format_record(results[0])
            print("Retrieved car rental by ID from database.")
            return formatted_results
        except Exception as e:
            print("Error getting car rental by ID from database: ", e)
            raise

    def create(self, rental_data):
        try:
            self.db_manager.execute_query(
                "INSERT INTO lyfter_car_rental.car_rental (user_id, car_id, rental_date_at, return_date_at, status) " \
                "VALUES (%s, %s, %s, %s, %s);",
                (
                    rental_data["user_id"],
                    rental_data["car_id"],
                    rental_data["rental_date_at"],
                    rental_data["return_date_at"],
                    rental_data["status"]
                )
            )
            print("Car rental created in database.")
        except Exception as e:
            print("Error creating car rental in database: ", e)
            raise

    def update(self, rental_id, rental_data):
        try:
            self.db_manager.execute_query(
                "UPDATE lyfter_car_rental.car_rental " \
                "SET user_id = %s, car_id = %s, rental_date_at = %s, return_date_at = %s, status = %s WHERE id = %s;",
                (
                    rental_data["user_id"],
                    rental_data["car_id"],
                    rental_data["rental_date_at"],
                    rental_data["return_date_at"],
                    rental_data["status"],
                    rental_id
                )
            )
            print("Car rental updated in database.")
        except Exception as e:
            print("Error updating car rental in database: ", e)
            raise

    def delete(self, rental_id):
        try:
            self.db_manager.execute_query(
                "DELETE FROM lyfter_car_rental.car_rental " \
                "WHERE id = %s;",
                (rental_id,)
            )
            print("Car rental deleted from database.")
        except Exception as e:
            print("Error deleting car rental from database: ", e)
            raise