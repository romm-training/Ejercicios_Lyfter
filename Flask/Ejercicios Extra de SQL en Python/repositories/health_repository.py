from exceptions import HealthRuleError

class HealthRepository:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def check_existing_tables(self):
        result = self.db_manager.execute_query(
            "SELECT 1 " \
            "FROM information_schema.tables " \
            "WHERE table_schema = 'lyfter_car_rental' " 
            "AND table_name IN ('car','car_rental','user');"
        )
        return result

    def get_record_quantity_in_car_table(self) -> int:
        result = self.db_manager.execute_query(
            "SELECT count(1) as cantidad_registros " \
            "FROM lyfter_car_rental.car;"
        )
        if not result:
            return 0
        else:
            return result[0][0]

    def check_connection(self) -> bool:
        return self.db_manager.ping()