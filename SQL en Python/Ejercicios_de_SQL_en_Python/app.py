from flask import Flask
import logging

from infrastructure.db import PgManager

from repositories.user_repository import UserRepository
from repositories.car_repository import CarRepository
from repositories.car_rental_repository import CarRentalRepository

from services.user_service import UserService
from services.car_service import CarService
from services.car_rental_service import CarRentalService

from routes.user_routes import register_user_routes
from routes.car_routes import register_car_routes
from routes.car_rental_routes import register_car_rental_routes

def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",    
    )

configure_logging()

app = Flask(__name__)

db_manager = PgManager(
    db_name="EjerciciosDeSqlEnPython",
    user="postgres",
    password="ClaveSimple123",
    host="localhost",
    port=5432
)

user_repository = UserRepository(db_manager)
car_repository = CarRepository(db_manager)
car_rental_repository = CarRentalRepository(db_manager)

user_service = UserService(user_repository)
car_service = CarService(car_repository)
car_rental_service = CarRentalService(car_rental_repository)

register_user_routes(app, user_service)
register_car_routes(app, car_service)
register_car_rental_routes(app, car_rental_service)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True)