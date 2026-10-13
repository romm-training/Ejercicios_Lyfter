from services.state_machine import guard, effect
from services.enums.statuses import CarRentalStatus
from exceptions import BusinessRuleError 

@guard("rental_is_pending")
def rental_is_pending(ctx):
    rental = ctx.repos["car_rental"].get_by_id_for_update(ctx.record["car_rental_id"])
    if rental["status"] != CarRentalStatus.PENDING:
        raise BusinessRuleError(f"La renta {rental['id']} no está pendiente.")

@guard("rental_is_active")
def rental_is_active(ctx):
    rental = ctx.repos["car_rental"].get_by_id_for_update(ctx.record["car_rental_id"])
    if rental["status"] != CarRentalStatus.ACTIVE:
        raise BusinessRuleError(f"La renta {rental['id']} no está activa.")

@guard("rental_is_completed")
def rental_is_completed(ctx):
    rental = ctx.repos["car_rental"].get_by_id_for_update(ctx.record["car_rental_id"])
    if rental["status"] != CarRentalStatus.COMPLETED:
        raise BusinessRuleError(f"La renta {rental['id']} no está completa.")

@guard("rental_is_cancelled")
def rental_is_cancelled(ctx):
    rental = ctx.repos["car_rental"].get_by_id_for_update(ctx.record["car_rental_id"])
    if rental["status"] != CarRentalStatus.CANCELLED:
        raise BusinessRuleError(f"La renta {rental['id']} no está cancelada.")

@guard("rental_is_overdue")
def rental_is_overdue(ctx):
    rental = ctx.repos["car_rental"].get_by_id_for_update(ctx.record["car_rental_id"])
    if rental["status"] != CarRentalStatus.OVERDUE:
        raise BusinessRuleError(f"La renta {rental['id']} no está vencida.")

@guard("user_has_no_active_rentals")
def user_has_no_active_rentals(ctx):
    rentals = ctx.repos["car_rental"].get_by_user_id_and_rental_status(ctx.record["id"], CarRentalStatus.ACTIVE)
    if rentals:
        raise BusinessRuleError(f"El usuario {ctx.record["id"]} tiene rentas activas o pendientes.")

@effect("rental_to_pending")
def rental_to_pending(ctx):
    ctx.repos["car_rental"].update_status(
        ctx.current_record["car_rental_id"], 
        CarRentalStatus.PENDING
    )

@effect("rental_to_active")
def rental_to_acive(ctx):
    ctx.repos["car_rental"].update_status(
        ctx.current_record["car_rental_id"], 
        CarRentalStatus.ACTIVE
    )

@effect("rental_to_completed")
def rental_to_completed(ctx):
    ctx.repos["car_rental"].update_status(
        ctx.current_record["car_rental_id"], 
        CarRentalStatus.COMPLETED
    )

@effect("rental_to_cancelled")
def rental_to_cancelled(ctx):
    ctx.repos["car_rental"].update_status(
        ctx.current_record["car_rental_id"], 
        CarRentalStatus.CANCELLED
    )

@effect("rental_to_overdue")
def rental_to_overdue(ctx):
    ctx.repos["car_rental"].update_status(
        ctx.current_record["car_rental_id"], 
        CarRentalStatus.OVERDUE
    )