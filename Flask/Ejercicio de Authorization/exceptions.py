class AppError(Exception):
    status_code = 500
    message = "Error interno de la aplicación."

class NotFoundError(AppError):
    status_code = 404
    message = "Registro no encontrado."

class AuthenticationError(AppError):
    status_code = 401
    message = "No autenticado."

class InvalidCredentialsError(AuthenticationError):
    message = "Credenciales inválidas."

class InvalidTokenError(AuthenticationError):
    message = "Token invalido o expirado."

class AuthorizationError(AppError):
    status_code = 403
    message = "No tiene permisos para realizar esta accion."

class InvalidFieldError(AppError):
    status_code = 400
    message = "Campo de entrada inválido."

class BusinessValidationError(AppError):
    status_code = 422
    message = "Error de validación."

class ConflictError(AppError):
    status_code = 409
    message = "El recurso entra en conflicto con uno existente (llave duplicada)."

class BusinessRuleError(AppError):
    status_code = 422

class ConfigurationError(Exception):
    """Configuración inválida al arrancar; no es un error HTTP."""