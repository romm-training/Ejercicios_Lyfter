from services.state_machine import guard, effect
from services.enums.statuses import CarStatus
from exceptions import BusinessRuleError 

def _car_id_helper(ctx):
    if ctx.entity == "car":
        return ctx.current_record["id"]
    source = ctx.current_record or ctx.data
    return source["car_id"]

@guard("car_is_available")
def car_is_available(ctx):
    car = ctx.repos["car"].get_by_id_for_update(_car_id_helper(ctx))
    if car["status"] != CarStatus.AVAILABLE:
        raise BusinessRuleError(f"El carro {car['id']} no está disponible.")

@guard("car_is_reserved")
def car_is_reserved(ctx):
    car = ctx.repos["car"].get_by_id_for_update(_car_id_helper(ctx))
    if car["status"] != CarStatus.RESERVED:
        raise BusinessRuleError(f"El carro {car['id']} no está reservado.")

@guard("car_is_rented")
def car_is_rented(ctx):
    car = ctx.repos["car"].get_by_id_for_update(_car_id_helper(ctx))
    if car["status"] != CarStatus.RENTED:
        raise BusinessRuleError(f"El carro {car['id']} no está rentado.")

@guard("car_is_in_maintenance")
def car_is_in_maintenance(ctx):
    car = ctx.repos["car"].get_by_id_for_update(_car_id_helper(ctx))
    if car["status"] != CarStatus.MAINTENANCE:
        raise BusinessRuleError(f"El carro {car['id']} no está en mantenimiento.")

@guard("car_is_inactive")
def car_is_inactive(ctx):
    car = ctx.repos["car"].get_by_id_for_update(_car_id_helper(ctx))
    if car["status"] != CarStatus.INACTIVE:
        raise BusinessRuleError(f"El carro {car['id']} no está en inactivo.")

@guard("car_is_sold")
def car_is_sold(ctx):
    car = ctx.repos["car"].get_by_id_for_update(_car_id_helper(ctx))
    if car["status"] != CarStatus.SOLD:
        raise BusinessRuleError(f"El carro {car['id']} no está vendido.")

@effect("car_to_available")
def car_to_available(ctx):
    ctx.repos["car"].update_status(
        _car_id_helper(ctx), 
        CarStatus.AVAILABLE
    )

@effect("car_to_reserved")
def car_to_reserved(ctx):
    ctx.repos["car"].update_status(
        _car_id_helper(ctx), 
        CarStatus.RESERVED
    )

@effect("car_to_rented")
def car_to_rented(ctx):
    ctx.repos["car"].update_status(
        _car_id_helper(ctx), 
        CarStatus.RENTED
    )

@effect("car_to_maintenance")
def car_to_maintenance(ctx):
    ctx.repos["car"].update_status(
        _car_id_helper(ctx), 
        CarStatus.MAINTENANCE
    )

@effect("car_to_inactive")
def car_to_inactive(ctx):
    ctx.repos["car"].update_status(
        _car_id_helper(ctx), 
        CarStatus.INACTIVE
    )

@effect("car_to_sold")
def car_to_sold(ctx):
    ctx.repos["car"].update_status(
        _car_id_helper(ctx), 
        CarStatus.SOLD
    )