from exceptions import NotFoundError, BusinessRuleError

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

    def _all_or_none(self, results):
        if not results:
            return None
        formatted_results = [self._format_record(result) for result in results]
        return formatted_results

    def get_all(self, filters):
        _COLUMNS_ALLOWED_TO_FILTER = {"make","model","year","status"}

        filters = filters or {}
        invalid_filters = set(filters) - _COLUMNS_ALLOWED_TO_FILTER
        if invalid_filters:
            raise BusinessRuleError(f"Filtros inválidos: {invalid_filters}")

        select = "SELECT id, make, model, year, status " \
                "FROM lyfter_car_rental.car"

        where = " AND ".join(f"{f} = %s" for f in filters)

        query = select + (f" WHERE {where}" if where else ";")

        results = self.db_manager.execute_query(query, tuple(filters.values()))
        return self._all_or_raise(results)

    def get_by_id(self, car_id):
        results = self.db_manager.execute_query(
            "SELECT id, make, model, year, status " \
            "FROM lyfter_car_rental.car " \
            "WHERE id = %s;",
            (car_id,)
        )
        return self._first_or_raise(results, car_id)

    def get_by_id_for_update(self, car_id):
        results = self.db_manager.execute_query(
            "SELECT id, make, model, year, status " \
            "FROM lyfter_car_rental.car " \
            "WHERE id = %s" \
            "FOR UPDATE;",
            (car_id,)
        )
        return self._first_or_raise(results, car_id)

    def create(self, car_data):
        results = self.db_manager.execute_query(
            "INSERT INTO lyfter_car_rental.car (make, model, year) " \
            "VALUES (%s, %s, %s)" \
            "RETURNING *;",
            (
                car_data["make"],
                car_data["model"],
                car_data["year"]
            )
        )
        return self._first_or_none(results)

    def update(self, car_id, car_data):
        results = self.db_manager.execute_query(
            "UPDATE lyfter_car_rental.car " \
            "SET make = %s, model = %s, year = %s " \
            "WHERE id = %s" \
            "RETURNING *;",
            (
                car_data["make"],
                car_data["model"],
                car_data["year"],
                car_id
            )
        )
        return self._first_or_none(results)

    def update_status(self, car_id, target_status):
        results = self.db_manager.execute_query(
            "UPDATE lyfter_car_rental.car " \
            "SET status = %s " \
            "WHERE id = %s" \
            "RETURNING *;",
            (
                target_status,
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
