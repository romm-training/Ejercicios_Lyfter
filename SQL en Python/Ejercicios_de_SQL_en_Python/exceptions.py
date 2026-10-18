class AppError(Exception):
    status_code = 500
    message = "Error interno de la aplicación."

class NotFoundError(AppError):
    status_code = 404
    message = "Registro no encontrado."

class BusinessRuleError(AppError):
    status_code = 422

class InvalidTransitionError(AppError):
    status_code = 409