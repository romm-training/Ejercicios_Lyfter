from exceptions import BusinessRuleError
from repositories.base_repository import BaseRepository

class UserRepository(BaseRepository):
    _COLUMNS = ("id", "name", "email", "username", "birthdate_at", "account_status")
    _ENTITY_LABEL = "Usuario"
    _SELECT_COLUMNS = ", ".join(_COLUMNS)

    def _format_record(self, record):
        data = super()._format_record(record)
        data["password"] = "***"
        return data

    @staticmethod
    def get_table_name():
        return "user"

    @classmethod
    def get_field_names(cls):
        columns = list(cls._COLUMNS)
        columns.insert(columns.index("username") + 1, "password")
        return columns

    def get_all(self, filters=None):
        _COLUMNS_ALLOWED_TO_FILTER = set(self._COLUMNS) - {"id"}

        filters = filters or {}
        invalid_filters = set(filters) - _COLUMNS_ALLOWED_TO_FILTER
        if invalid_filters:
            raise BusinessRuleError(f"Filtros inválidos: {invalid_filters}")

        select = f"SELECT {self._SELECT_COLUMNS} " \
                "FROM lyfter_car_rental.user"

        where = " AND ".join(f"{f} = %s" for f in filters)

        query = select + (f" WHERE {where}" if where else ";")
        
        results = self.db_manager.execute_query(query, tuple(filters.values()))
        return self._format_all(results)

    def get_by_id(self, user_id):
        results = self.db_manager.execute_query(
            f"SELECT {self._SELECT_COLUMNS} " \
            "FROM lyfter_car_rental.user " \
            "WHERE id = %s;",
            (user_id,)
        )
        return self._first_or_raise(results, user_id)

    def get_by_id_for_update(self, user_id):
        results = self.db_manager.execute_query(
            f"SELECT {self._SELECT_COLUMNS} " \
            "FROM lyfter_car_rental.user " \
            "WHERE id = %s " \
            "FOR UPDATE;",
            (user_id,)
        )
        return self._first_or_raise(results, user_id)

    def get_by_username_or_email_for_update(self, username, email):
        results = self.db_manager.execute_query(
            f"SELECT {self._SELECT_COLUMNS} " \
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
            f"RETURNING {self._SELECT_COLUMNS};",
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
            "WHERE id = %s " \
            f"RETURNING {self._SELECT_COLUMNS};",
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
            "WHERE id = %s " \
            f"RETURNING {self._SELECT_COLUMNS};",
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

    