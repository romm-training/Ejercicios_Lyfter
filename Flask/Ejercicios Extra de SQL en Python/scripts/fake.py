from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker("es_MX")

def fake_user():
    account_statuses = ["Active", "Inactive", "Delinquent"]

    return {
        "name": fake.name(),
        "email": fake.email(),
        "username": fake.user_name()[0:20],
        "password": fake.password(length=10)[0:20],
        "birthdate_at": fake.date_of_birth(minimum_age=18, maximum_age=70),
        "account_status": random.choice(account_statuses)
    }

def fake_car():
    status = ["available", "reserved", "rented", "maintenance", "inactive", "sold"]
    car_catalog = {
        "Toyota": ["Corolla", "Camry", "Yaris", "Hilux"],
        "Honda": ["Civic", "Accord", "CR-V", "Fit"],
        "Ford": ["Focus", "Fusion", "Mustang", "Escape"],
        "Chevrolet": ["Cruze", "Malibu", "Equinox", "Spark"],
        "Nissan": ["Sentra", "Altima", "Rogue", "Versa"],
        "Hyundai": ["Elantra", "Sonata", "Tucson", "Santa Fe"],
        "Kia": ["Rio", "Optima", "Sportage", "Sorento"],
        "Volkswagen": ["Jetta", "Golf", "Passat", "Tiguan"],
        "Mazda": ["Mazda3", "Mazda6", "CX-5", "CX-9"],
        "Subaru": ["Impreza", "Legacy", "Forester", "Outback"]
    }

    make = random.choice(list(car_catalog.keys()))
    model = random.choice(car_catalog[make])
    year = random.randint(2005,2026)

    return {
        "make": make,
        "model": model,
        "year": year,
        "status": random.choice(status)
    }
    

def fake_car_rental(car_id, user_id):
    status = ["pending", "active", "completed", "cancelled", "overdue"]

    rental_date = fake.past_date(start_date="-15d")
    return_date = rental_date + timedelta(days=random.randint(1,10))

    return {
        "car_id": car_id,
        "user_id": user_id,
        "rental_date_at": rental_date,
        "return_date_at": return_date,
        "status": random.choice(status)
    }