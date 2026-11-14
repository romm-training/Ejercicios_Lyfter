import logging, os, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from functools import partial
from dotenv import load_dotenv
from pydantic import ValidationError

from ejercicio3.dtos.address_dto import AddressDTO, AddressCreateDTO, AddressUpdateDTO
from ejercicio3.dtos.user_dto import UserDTO, UserCreateDTO, UserUpdateDTO, UserReadDTO
from ejercicio3.dtos.car_dto import CarDTO, CarCreateDTO, CarUpdateDTO
from ejercicio3.exceptions import InvalidFieldError, NotFoundError, ConflictError
from ejercicio3.infrastructure.db import create_session_factory
from ejercicio3.repositories.unit_of_work import UnitOfWork
from ejercicio3.services.address_service import AddressService
from ejercicio3.services.user_service import UserService
from ejercicio3.services.car_service import CarService

logger = logging.getLogger(__name__)

def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

def get_database_url() -> str:
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL no está configurada en las variables de entorno.")
    return url

def build_address_service() -> AddressService:
    session_factory = create_session_factory(get_database_url())
    return AddressService(partial(UnitOfWork, session_factory))

def build_user_service() -> UserService:
    session_factory = create_session_factory(get_database_url())
    return UserService(partial(UnitOfWork, session_factory))

def build_car_service() -> CarService:
    session_factory = create_session_factory(get_database_url())
    return CarService(partial(UnitOfWork, session_factory))

def run_user_demo(service: UserService) -> int:
    logger.info("---- Paso 1: Crear Usuario ----")
    created = service.create_user(
        UserCreateDTO(
            name="Nombre",
            full_name="Nombre Prueba"
        )
    )
    logger.info(f"Usuario creado: {created}")

    logger.info("---- Paso 2: Listar Usuarios ----")
    users = service.get_all()
    if users:
        logger.info("Lista de usuarios almacenados: ")
        [logger.info(user) for user in users]

    logger.info("---- Paso 3: Obtener Usuario ----")
    user = service.get_by_id(created.id)
    logger.info(f"Usuario {created.id}: {user}")

    logger.info("---- Paso 4: Actualizar Usuario ----")
    updated = service.update_user(
        created.id,
        UserUpdateDTO(
            name="Nuevo",
            full_name="Nuevo Nombre"
        )
    )
    logger.info(f"Usuario actualizado: {updated}")

    user = service.get_by_id(created.id)
    logger.info(f"Usuario {created.id} despues de actualizar: {user}")

    return created.id
    
def run_address_demo(service: AddressService, user_id: int) -> int:
    logger.info("---- Paso 5: Crear Direccion ----")
    created = service.create_address(
        AddressCreateDTO(
            user_id=user_id, 
            email_address="john.doe@example.com"
        )
    )
    logger.info(f"Dirección creada: {created}")

    logger.info("---- Paso 6: Listar Direcciones ----")
    addresses = service.get_all()
    if addresses:
        logger.info("Lista de direcciones almacenadas: ")
        [logger.info(address) for address in addresses]

    logger.info("---- Paso 7: Obtener Direccion ----")
    address = service.get_by_id(created.id)
    logger.info(f"Dirreccion {created.id}: {address}")

    logger.info("---- Paso 8: Actualizar Direccion ----")
    updated = service.update_address(
        created.id, 
        AddressUpdateDTO(email_address="jane.doe@example.com")
    )
    logger.info(f"Dirección actualizada: {updated}")

    address = service.get_by_id(created.id)
    logger.info(f"Dirreccion {created.id} despues de actualizar: {address}")

    return created.id

def run_car_demo(service: CarService) -> int:
    logger.info("---- Paso 9: Crear Carro ----")
    created = service.create_car(
        CarCreateDTO(
            plate="123456",
            make="Toyota",
            model="Yaris",
            year=2010
        )
    )
    logger.info(f"Carro creado: {created}")

    logger.info("---- Paso 10: Listar Carros ----")
    cars = service.get_all()
    if cars:
        logger.info("Lista de carros almacenados: ")
        [logger.info(car) for car in cars]

    logger.info("---- Paso 11: Obtener Carro ----")
    car = service.get_by_id(created.id)
    logger.info(f"Carro {created.id}: {car}")

    logger.info("---- Paso 12: Actualizar Carro ----")
    updated = service.update_car(
        created.id,
        CarUpdateDTO(
            plate="654321",
            make="Nissan",
            model="Sentra",
            year=2015
        )
    )
    logger.info(f"Carro actualizado: {updated}")

    car = service.get_by_id(created.id)
    logger.info(f"Carro {created.id} despues de actualizar: {car}")

    return created.id

def run_user_car_association(service: UserService
                             , user_id: int
                             , car_id: int) -> None:
    logger.info("---- Paso 13: Asociar Usuario y Carro ----")
    user_full_info = service.associate_car(
        user_id=user_id,
        car_id=car_id
    )
    logger.info(f"User and associations: {user_full_info}")

def run_delete_run_delete_user_car_association(service: UserService
                                               , user_id: int
                                               , car_id: int) -> None:
    logger.info("---- Paso 14: Eliminar Asociacion Usuario y Carro ----")
    service.disassociate_car(
        user_id=user_id,
        car_id=car_id
    )
    logger.info(f"Asociacion de Usuario {user_id} con Carro {car_id} eliminada")

def run_delete_car(service: CarService, car_id: int) -> None:
    logger.info("---- Paso 15: Eliminar Carro ----")
    service.delete_car(car_id)
    logger.info(f"Carro {car_id} eliminada")

def run_delete_address(service: AddressService, address_id: int) -> None:
    logger.info("---- Paso 16: Eliminar Direccion ----")
    service.delete_address(address_id)
    logger.info(f"Dirección {address_id} eliminada")

def run_delete_user(service: UserService, user_id: int) -> None:
    logger.info("---- Paso 17: Eliminar Usuario ----")
    service.delete_user(user_id)
    logger.info(f"Usuario {user_id} eliminado")

def main() -> None:
    load_dotenv()
    configure_logging()

    user_service = build_user_service()
    address_service = build_address_service()
    car_service = build_car_service()
    
    try:
        user_id = run_user_demo(user_service)
        address_id = run_address_demo(address_service, user_id)
        car_id = run_car_demo(car_service)
        run_user_car_association(user_service, user_id, car_id)

        run_delete_run_delete_user_car_association(user_service, user_id, car_id)
        run_delete_car(car_service, car_id)
        run_delete_address(address_service, address_id)
        run_delete_user(user_service, user_id)

    except ValidationError as ve:
        logger.error(f"Datos inválidos: {ve}")
    except (NotFoundError, InvalidFieldError, ConflictError) as nfe:
        logger.error(f"Operación rechazada: {nfe}")
    except Exception as e:
        logger.error(f"Excepcion general: {e}")

if __name__ == "__main__":
    main()
