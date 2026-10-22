from flask import Flask
import logging, os
from dotenv import load_dotenv

load_dotenv()

from infrastructure.db import PgManager
from infrastructure.backup_writer import BackupWriter
from infrastructure.csv_backup_writer import CsvBackupWriter

from repositories.user_repository import UserRepository
from repositories.car_repository import CarRepository
from repositories.car_rental_repository import CarRentalRepository

from services.user_service import UserService
from services.car_service import CarService
from services.car_rental_service import CarRentalService
from services.state_machine import build_state_machine
from services.backup_service import BackupService

from routes.error_handlers import register_error_handlers

from routes.user_routes import register_user_routes
from routes.car_routes import register_car_routes
from routes.car_rental_routes import register_car_rental_routes
from routes.backup_routes import register_backup_routes

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

user_service = UserService(user_repository, state_machine, db_manager)
car_service = CarService(car_repository, state_machine, db_manager)
car_rental_service = CarRentalService(car_rental_repository, state_machine, db_manager)

repositories_to_backup = [
    user_repository,
    car_repository,
    car_rental_repository
]

backup_path = os.environ["BACKUP_PATH"]
backup_writer = os.environ["BACKUP_WRITER"]

BACKUP_WRITERS = {
    "csv": "CsvBackupWriter"
}

csv_writer = CsvBackupWriter(backup_path)

backup_service = BackupService(
    repositories_to_backup, 
    BACKUP_WRITERS[backup_writer]
)

register_error_handlers(app)

register_user_routes(app, user_service)
register_car_routes(app, car_service)
register_car_rental_routes(app, car_rental_service)
register_backup_routes(app, backup_service )

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True)