class NotFoundError(Exception):
    pass

class InvalidFieldError(Exception):
    pass

class ValidationError(Exception):
    """Dato de entrada inválido según las reglas de negocio."""

class ConflictError(Exception):
    """Captura integridad en base de datos."""