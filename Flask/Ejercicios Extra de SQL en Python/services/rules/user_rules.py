from services.state_machine import guard, effect
from services.enums.statuses import UserStatus
from exceptions import BusinessRuleError 

def _user_id_helper(ctx):
    if ctx.entity == "user":
        return ctx.current_record["id"]
    source = ctx.current_record or ctx.data
    return source["user_id"]

@guard("user_is_active")
def user_is_active(ctx):
    user_id = _user_id_helper(ctx)
    user = ctx.repos["user"].get_by_id_for_update(user_id)
    if user["account_status"] != UserStatus.ACTIVE:
        raise BusinessRuleError(f"El usuario {user['id']} no está activo.")

@guard("user_is_inactive")
def user_is_inactive(ctx):
    user_id = _user_id_helper(ctx)
    user = ctx.repos["user"].get_by_id_for_update(user_id)
    if user["account_status"] != UserStatus.INACTIVE:
        raise BusinessRuleError(f"El usuario {user['id']} no está inactivo.")

@guard("user_is_delinquent")
def user_is_delinquent(ctx):
    user_id = _user_id_helper(ctx)
    user = ctx.repos["user"].get_by_id_for_update(user_id)
    if user["account_status"] != UserStatus.DELINQUENT:
        raise BusinessRuleError(f"El usuario {user['id']} no está moroso.")

@guard("username_and_email_no_exist")
def username_and_email_no_exist(ctx):
    username = ctx.current_record["username"] if ctx.current_record else ctx.data["username"]
    email = ctx.current_record["email"] if ctx.current_record else ctx.data["email"]
    result = ctx.repos["user"].get_by_username_or_email_for_update(username, email)
    if result:
        raise BusinessRuleError(f"El username o email ya existen.")

@effect("user_to_active")
def user_to_active(ctx):
    user_id = _user_id_helper(ctx)
    ctx.repos["user"].update_status(
        user_id, 
        UserStatus.ACTIVE
    )

@effect("user_to_inactive")
def user_to_inactive(ctx):
    user_id = _user_id_helper(ctx)
    ctx.repos["user"].update_status(
        user_id, 
        UserStatus.INACTIVE
    )

@effect("user_to_delinquent")
def user_to_delinquent(ctx):
    user_id = _user_id_helper(ctx)
    ctx.repos["user"].update_status(
        user_id, 
        UserStatus.DELINQUENT
    )
