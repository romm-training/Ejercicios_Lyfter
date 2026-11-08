class ConfigurationError(Exception):
    """Configuración inválida al arrancar; no es un error HTTP."""

class AppError(Exception):
    pass

class NotFoundError(AppError):
    pass

class BusinessRuleError(AppError):
    pass

class InvalidTransitionError(AppError):
    pass

class BackupError(AppError):
    pass

class HealthRuleError(Exception):
    pass
