from exceptions import NotFoundError, BusinessRuleError

class UserRepository:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def _format_record(self, user_record):
        return {
            "id": user_record[0],
            "name": user_record[1],
            "email": user_record[2],
            "username": user_record[3],
            "password": "***",
            "birthdate_at": user_record[4],
            "account_status": user_record[5]
        }

    def _first_or_raise(self, results, user_id):
        if not results:
            raise NotFoundError(f"Usuario {user_id} no encontrado.")
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

    def get_all(self, filters=None):
        _COLUMNS_ALLOWED_TO_FILTER = {"name","email","username","birthdate_at","account_status"}

        filters = filters or {}
        invalid_filters = set(filters) - _COLUMNS_ALLOWED_TO_FILTER
        if invalid_filters:
            raise BusinessRuleError(f"Filtros inválidos: {invalid_filters}")

        select = "SELECT id, name, email, username, birthdate_at, account_status " \
                "FROM lyfter_car_rental.user"

        where = " AND ".join(f"{f} = %s" for f in filters)

        query = select + (f" WHERE {where}" if where else ";")
        
        results = self.db_manager.execute_query(query, tuple(filters.values()))
        return self._all_or_raise(results)

    def get_by_id(self, user_id):
        results = self.db_manager.execute_query(
            "SELECT id, name, email, username, birthdate_at, account_status " \
            "FROM lyfter_car_rental.user " \
            "WHERE id = %s;",
            (user_id,)
        )
        return self._first_or_raise(results, user_id)

    def get_by_id_for_update(self, user_id):
        results = self.db_manager.execute_query(
            "SELECT id, name, email, username, birthdate_at, account_status " \
            "FROM lyfter_car_rental.user " \
            "WHERE id = %s " \
            "FOR UPDATE;",
            (user_id,)
        )
        return self._first_or_raise(results, user_id)

    def get_by_username_or_email_for_update(self, username, email):
        results = self.db_manager.execute_query(
            "SELECT id, name, email, username, birthdate_at, account_status " \
            "FROM lyfter_car_rental.user " \
            "WHERE username = %s OR email = %s " \
            "FOR UPDATE;",
            (username, email)
        )
        return self._first_or_none(results)

    def create(self, user_data):
        results = self.db_manager.execute_query(
            "INSERT INTO lyfter_car_rental.user (name, email, username, password, birthdate_at, account_status) " \
            "VALUES (%s, %s, %s, %s, %s, %s) " \
            "RETURNING id, name, email, username, birthdate_at, account_status;",
            (
                user_data["name"],
                user_data["email"],
                user_data["username"],
                user_data["password"],
                user_data["birthdate_at"],
                user_data["account_status"]
            )
        )
        return self._first_or_none(results)

    def update(self, user_id, user_data):
        results = self.db_manager.execute_query(
            "UPDATE lyfter_car_rental.user " \
            "SET name = %s, email = %s, username = %s, password = %s, birthdate_at = %s " \
            "WHERE id = %s" \
            "RETURNING id, name, email, username, birthdate_at, account_status;",
            (
                user_data["name"],
                user_data["email"],
                user_data["username"],
                user_data["password"],
                user_data["birthdate_at"],
                user_id
            )
        )
        return self._first_or_none(results)

    def update_status(self, user_id, target_status):
        results = self.db_manager.execute_query(
            "UPDATE lyfter_car_rental.user " \
            "SET account_status = %s " \
            "WHERE id = %s" \
            "RETURNING id, name, email, username, birthdate_at, account_status;",
            (
                target_status,
                user_id
            )
        )
        return self._first_or_none(results)

    def delete(self, user_id):
        self.db_manager.execute_query(
            "DELETE FROM lyfter_car_rental.user " \
            "WHERE id = %s;",
            (user_id,)
        )

    