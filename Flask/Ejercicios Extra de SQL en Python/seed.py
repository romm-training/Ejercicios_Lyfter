from dotenv import load_dotenv
from infrastructure.db import PgManager
import random

from repositories.car_repository import CarRepository
from repositories.user_repository import UserRepository
from repositories.car_rental_repository import CarRentalRepository

from scripts.fake import fake_user, fake_car, fake_car_rental

load_dotenv()

db = PgManager.from_env()

try:
    car_repository = CarRepository(db)
    user_repository = UserRepository(db)
    car_rental_repository = CarRentalRepository(db)

    created_users = []
    created_cars = []
    created_car_rentals = []

    with db.transaction():
        for _ in range(200):
            created_users.append(user_repository.create(fake_user()))

        for _ in range(100):
            created_cars.append(car_repository.create(fake_car()))

        for _ in range(50):
            selected_user = random.choice(created_users)
            selected_car = random.choice(created_cars)

            created_car_rentals.append(
                car_rental_repository.create(
                    fake_car_rental(
                        selected_car["id"],
                        selected_user["id"] 
                    )
                )
            )

        print("--------- Usuarios creados ---------")
        print(created_users)
        print("--------- Carros creados ---------")
        print(created_cars)
        print("--------- Rentas creadas ---------")
        print(created_car_rentals)
finally:
    db.close_connection()