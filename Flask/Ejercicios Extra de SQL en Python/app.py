from flask import Flask
import logging, os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from infrastructure.db import PgManager
from infrastructure.backup_writer_factory import create_backup_writer

from repositories.user_repository import UserRepository
from repositories.car_repository import CarRepository
from repositories.car_rental_repository import CarRentalRepository
from repositories.health_repository import HealthRepository

from services.user_service import UserService
from services.car_service import CarService
from services.car_rental_service import CarRentalService
from services.state_machine import build_state_machine
from services.backup_service import BackupService
from services.rules.health_rules import DbConnectionCheck, RequiredTablesCheck, CarsTableRecordQuantityCheck
from services.health_service import HealthService

from routes.error_handlers import register_error_handlers

from routes.user_routes import register_user_routes
from routes.car_routes import register_car_routes
from routes.car_rental_routes import register_car_rental_routes
from routes.backup_routes import register_backup_routes
from routes.health_routes import register_health_routes

def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",    
    )

configure_logging()

app = Flask(__name__)

db_manager = PgManager.from_env()

state_machine = build_state_machine(db_manager)

user_repository = UserRepository(db_manager)
car_repository = CarRepository(db_manager)
car_rental_repository = CarRentalRepository(db_manager)
health_repository = HealthRepository(db_manager)

user_service = UserService(user_repository, state_machine, db_manager)
car_service = CarService(car_repository, state_machine, db_manager)
car_rental_service = CarRentalService(car_rental_repository, state_machine, db_manager)

repositories_to_backup = [
    user_repository,
    car_repository,
    car_rental_repository
]

backup_path = Path(os.environ["BACKUP_PATH"]).resolve()
backup_writer_type = os.environ["BACKUP_WRITER_TYPE"]

backup_writer = create_backup_writer(
    backup_writer_type,
    backup_path
)
backup_service = BackupService(
    repositories_to_backup, 
    backup_writer
)

health_service = HealthService(
    [
        DbConnectionCheck(health_repository),
        RequiredTablesCheck(health_repository),
        CarsTableRecordQuantityCheck(health_repository)
    ]
)

register_error_handlers(app)

register_user_routes(app, user_service)
register_car_routes(app, car_service)
register_car_rental_routes(app, car_rental_service)
register_backup_routes(app, backup_service )
register_health_routes(app, health_service)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True)