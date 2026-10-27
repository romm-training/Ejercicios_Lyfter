from exceptions import NotFoundError, BusinessRuleError

class CarRentalRepository():
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def _format_record(self, car_rental_record):
        return {
            "id": car_rental_record[0],
            "car_id": car_rental_record[1],
            "user_id": car_rental_record[2],
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

    def _format_all(self, results):
        formatted_results = [self._format_record(result) for result in results]
        return formatted_results

    def _all_or_none(self, results):
        if not results:
            return None
        formatted_results = [self._format_record(result) for result in results]
        return formatted_results

    @staticmethod
    def get_table_name():
        return "car_rental"

    @staticmethod
    def get_field_names():
        return [
            "id",
            "car_id",
            "user_id",
            "rental_date_at",
            "return_date_at",
            "status"
        ]
    
    def get_all(self, filters):
        _COLUMNS_ALLOWED_TO_FILTER = {"user_id","car_id","rental_date_at","return_date_at","status"}

        filters = filters or {}
        invalid_filters = set(filters) - _COLUMNS_ALLOWED_TO_FILTER
        if invalid_filters:
            raise BusinessRuleError(f"Filtros inválidos: {invalid_filters}")

        select = "SELECT id, car_id, user_id, rental_date_at, return_date_at, status " \
                "FROM lyfter_car_rental.car_rental"

        where = " AND ".join(f"{f} = %s" for f in filters)

        query = select + (f" WHERE {where}" if where else ";")
        
        results = self.db_manager.execute_query(query, tuple(filters.values()))
        return self._format_all(results)

    def get_by_id(self, rental_id):
        results = self.db_manager.execute_query(
            "SELECT id, car_id, user_id, rental_date_at, return_date_at, status " \
            "FROM lyfter_car_rental.car_rental " \
            "WHERE id = %s;",
            (rental_id,)
        )
        return self._first_or_raise(results, rental_id)

    def get_by_id_for_update(self, rental_id):
        results = self.db_manager.execute_query(
            "SELECT id, car_id, user_id, rental_date_at, return_date_at, status " \
            "FROM lyfter_car_rental.car_rental " \
            "WHERE id = %s " \
            "FOR UPDATE;",
            (rental_id,)
        )
        return self._first_or_raise(results, rental_id)

    def get_by_user_id_and_rental_status(self, user_id, status):
        results = self.db_manager.execute_query(
            "SELECT id, car_id, user_id, rental_date_at, return_date_at, status " \
            "FROM lyfter_car_rental.car_rental " \
            "WHERE user_id = %s AND status = %s " \
            "FOR UPDATE;",
            (user_id, status)
        )
        return self._all_or_none(results)

    def get_by_user_id_and_multiple_rental_status(self, user_id, statuses):
        statuses_filter = ','.join(['%s'] * len(statuses))
        query = f"""
                SELECT id, car_id, user_id, rental_date_at, return_date_at, status 
                FROM lyfter_car_rental.car_rental  
                WHERE user_id = %s AND status IN ({statuses_filter})  
                FOR UPDATE;
                """
        params = [user_id] + statuses

        results = self.db_manager.execute_query(query, params)
        return self._all_or_none(results)

    def get_by_car_id_and_rental_status(self, car_id, status):
        results = self.db_manager.execute_query(
            "SELECT id, car_id, user_id, rental_date_at, return_date_at, status " \
            "FROM lyfter_car_rental.car_rental " \
            "WHERE car_id = %s AND status = %s " \
            "FOR UPDATE;",
            (car_id, status)
        )
        return self._all_or_none(results)

    def create(self, rental_data):
        results = self.db_manager.execute_query(
            "INSERT INTO lyfter_car_rental.car_rental (user_id, car_id, return_date_at, status) " \
            "VALUES (%s, %s, %s, %s) " \
            "RETURNING id, car_id, user_id, rental_date_at, return_date_at, status;",
            (
                rental_data["user_id"],
                rental_data["car_id"],
                rental_data["return_date_at"],
                rental_data["status"]
            )
        )
        return self._first_or_none(results)

    def update(self, rental_id, rental_data):
        results = self.db_manager.execute_query(
            "UPDATE lyfter_car_rental.car_rental " \
            "SET return_date_at = %s " \
            "WHERE id = %s " \
            "RETURNING id, car_id, user_id, rental_date_at, return_date_at, status;",
            (
                rental_data["return_date_at"],
                rental_id
            )
        )
        return self._first_or_none(results)

    def update_status(self, rental_id, target_status):
        results = self.db_manager.execute_query(
            "UPDATE lyfter_car_rental.car_rental " \
            "SET status = %s " \
            "WHERE id = %s " \
            "RETURNING id, car_id, user_id, rental_date_at, return_date_at, status;",
            (
                target_status,
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
