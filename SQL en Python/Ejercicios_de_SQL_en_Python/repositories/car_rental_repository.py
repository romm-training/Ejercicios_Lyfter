from exceptions import NotFoundError

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

    def _first_or_raise(self, results, rental_id):
        if not results:
            raise NotFoundError(f"Registro {rental_id} no encontrado.")
        return self._format_record(results[0])

    def _first_or_none(self, results):
        if not results:
            return None
        return self._format_record(results[0])

    def _all_or_raise(self, results):
        if not results:
            raise NotFoundError(f"No se han encontrado registros.")
        formatted_results = [self._format_record(result) for result in results]
        return formatted_results

    def get_all(self):
        results = self.db_manager.execute_query(
            "SELECT id, user_id, car_id, rental_date_at, return_date_at, status " \
            "FROM lyfter_car_rental.car_rental;"
        )
        print("Retornar todas las rentas.")
        return self._all_or_raise(results)

    def get_by_id(self, rental_id):
        results = self.db_manager.execute_query(
            "SELECT id, user_id, car_id, rental_date_at, return_date_at, status " \
            "FROM lyfter_car_rental.car_rental " \
            "WHERE id = %s;",
            (rental_id,)
        )
        print("Retornar renta por id.")
        return self._first_or_raise(results)

    def get_by_id_for_update(self, rental_id):
        results = self.db_manager.execute_query(
            "SELECT id, user_id, car_id, rental_date_at, return_date_at, status " \
            "FROM lyfter_car_rental.car_rental " \
            "WHERE id = %s" \
            "FOR UPDATE;",
            (rental_id,)
        )
        return self._first_or_raise(results)

    def get_by_user_id_and_rental_status(self, user_id, status):
        results = self.db_manager.execute_query(
            "SELECT id, user_id, car_id, rental_date_at, return_date_at, status " \
            "FROM lyfter_car_rental.car_rental " \
            "WHERE user_id = %s AND status = %s" \
            "FOR UPDATE;",
            (user_id, status)
        )
        return self._all_or_raise(results)

    def create(self, rental_data):
        results = self.db_manager.execute_query(
            "INSERT INTO lyfter_car_rental.car_rental (user_id, car_id, rental_date_at, return_date_at, status) " \
            "VALUES (%s, %s, %s, %s, %s)" \
            "RETURNING *;",
            (
                rental_data["user_id"],
                rental_data["car_id"],
                rental_data["rental_date_at"],
                rental_data["return_date_at"],
                rental_data["status"]
            )
        )
        return self._first_or_none(results)

    def update(self, rental_id, rental_data):
        results = self.db_manager.execute_query(
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
        return self._first_or_none(results)

    def delete(self, rental_id):
        self.db_manager.execute_query(
            "DELETE FROM lyfter_car_rental.car_rental " \
            "WHERE id = %s;",
            (rental_id,)
        )
        print("Car rental deleted from database.")
