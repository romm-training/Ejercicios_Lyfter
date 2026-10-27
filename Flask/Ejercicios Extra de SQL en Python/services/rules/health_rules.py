from abc import ABC, abstractmethod
from exceptions import HealthRuleError

class HealthCheck(ABC):
    name: str

    @abstractmethod
    def run(self) -> None:
        """Lanza HealthRuleError si el chequeo falla."""

class DbConnectionCheck(HealthCheck):
    name = "db_connection"
    def __init__(self, repository):
        self.repository = repository

    def run(self):
        if not self.repository.check_connection():
            raise HealthRuleError("No hay conexion con la base de datos.")

class RequiredTablesCheck(HealthCheck):
    name = "required_tables"
    def __init__(self, repository):
        self.repository = repository

    def run(self):
        if len(self.repository.check_existing_tables()) != 3:
            raise HealthRuleError("Faltan tablas requeridas.")

class CarsTableRecordQuantityCheck(HealthCheck):
    name = "car_table_record_quantity"
    def __init__(self, repository):
        self.repository = repository

    def run(self):
        if self.repository.get_record_quantity_in_car_table() == 0:
            raise HealthRuleError("No hay registros en la tabla de carros.")
        
