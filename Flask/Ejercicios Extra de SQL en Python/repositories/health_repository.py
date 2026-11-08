class HealthRepository:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def check_existing_tables(self, tables):
        result = self.db_manager.execute_query(
            "SELECT table_name "
            "FROM information_schema.tables "
            "WHERE table_schema = 'lyfter_car_rental' "
            "AND table_name = ANY(%s);",
            (list(tables),)
        )
        return result or []

    def get_count_of_available_cars(self) -> int:
        result = self.db_manager.execute_query(
            "SELECT count(1) as cantidad_registros " \
            "FROM lyfter_car_rental.car " \
            "WHERE status = 'available';"
        )
        if not result:
            return 0
        else:
            return result[0][0]

    def check_connection(self) -> bool:
        return self.db_manager.ping()