from exceptions import BusinessRuleError
from repositories.base_repository import BaseRepository

class CarRepository(BaseRepository):
    _COLUMNS = ("id", "make", "model", "year", "status")
    _ENTITY_LABEL = "Auto"
    _SELECT_COLUMNS = ", ".join(_COLUMNS)

    @staticmethod
    def get_table_name():
        return "car"

    @classmethod
    def get_field_names(cls):
        return list(cls._COLUMNS)

    def get_all(self, filters=None):
        _COLUMNS_ALLOWED_TO_FILTER = set(self._COLUMNS) - {"id"}

        filters = filters or {}
        invalid_filters = set(filters) - _COLUMNS_ALLOWED_TO_FILTER
        if invalid_filters:
            raise BusinessRuleError(f"Filtros inválidos: {invalid_filters}")

        select = f"SELECT {self._SELECT_COLUMNS} " \
                "FROM lyfter_car_rental.car"

        where = " AND ".join(f"{f} = %s" for f in filters)

        query = select + (f" WHERE {where}" if where else ";")

        results = self.db_manager.execute_query(query, tuple(filters.values()))
        return self._format_all(results)

    def get_by_id(self, car_id):
        results = self.db_manager.execute_query(
            f"SELECT {self._SELECT_COLUMNS} " \
            "FROM lyfter_car_rental.car " \
            "WHERE id = %s;",
            (car_id,)
        )
        return self._first_or_raise(results, car_id)

    def get_by_id_for_update(self, car_id):
        results = self.db_manager.execute_query(
            f"SELECT {self._SELECT_COLUMNS} " \
            "FROM lyfter_car_rental.car " \
            "WHERE id = %s " \
            "FOR UPDATE;",
            (car_id,)
        )
        return self._first_or_raise(results, car_id)

    def create(self, car_data):
        results = self.db_manager.execute_query(
            "INSERT INTO lyfter_car_rental.car (make, model, year, status) " \
            "VALUES (%s, %s, %s, %s) " \
            f"RETURNING {self._SELECT_COLUMNS};",
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
            "SET make = %s, model = %s, year = %s " \
            "WHERE id = %s " \
            f"RETURNING {self._SELECT_COLUMNS};",
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
            "WHERE id = %s " \
            f"RETURNING {self._SELECT_COLUMNS};",
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
