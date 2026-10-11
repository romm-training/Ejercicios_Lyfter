from exceptions import NotFoundError

class CarRepository():
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def _format_record(self, car_record):
        return {
            "id": car_record[0],
            "make": car_record[1],
            "model": car_record[2],
            "year": car_record[3],
            "status": car_record[4]
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
            "SELECT id, make, model, year, status " \
            "FROM lyfter_car_rental.car;"
        )
        return self._all_or_raise(results)

    def get_by_id(self, car_id):
        results = self.db_manager.execute_query(
            "SELECT id, make, model, year, status " \
            "FROM lyfter_car_rental.car " \
            "WHERE id = %s;",
            (car_id,)
        )
        return self._first_or_raise(results, car_id)

    def create(self, car_data):
        results = self.db_manager.execute_query(
            "INSERT INTO lyfter_car_rental.car (make, model, year, status) " \
            "VALUES (%s, %s, %s, %s)" \
            "RETURNING *;",
            (
                car_data["make"],
                car_data["model"],
                car_data["year"],
                car_data["status"]
            )
        )
        return self._first_or_none(results)

    def update(self, car_id, car_data):
        results = self.db_manager.execute_query(
            "UPDATE lyfter_car_rental.car " \
            "SET make = %s, model = %s, year = %s, status = %s WHERE id = %s" \
            "RETURNING *;",
            (
                car_data["make"],
                car_data["model"],
                car_data["year"],
                car_data["status"],
                car_id
            )
        )
        return self._first_or_none(results)

    def delete(self, car_id):
        self.db_manager.execute_query(
            "DELETE FROM lyfter_car_rental.car " \
            "WHERE id = %s;",
            (car_id,)
        )
