class NotFoundError(Exception):
    pass

class InvalidFieldError(Exception):
    pass

class ValidationError(Exception):
    """Dato de entrada inválido según las reglas de negocio."""

class ConflictError(Exception):
    """El recurso entra en conflicto con uno existente (llave duplicada)."""