import logging
from flask import jsonify
from werkzeug.exceptions import HTTPException
from exceptions import (
    AppError, BackupError, BusinessRuleError, InvalidTransitionError, NotFoundError,
)

logger = logging.getLogger(__name__)

STATUS_CODES = {
    NotFoundError: 404,
    BusinessRuleError: 422,
    InvalidTransitionError: 409,
    BackupError: 500,
}

DEFAULT_MESSAGES = {
    NotFoundError: "Registro no encontrado.",
}

DEFAULT_STATUS_CODE = 500
DEFAULT_MESSAGE = "Error interno de la aplicación."


def _lookup(table: dict, exc: Exception, default):
    for cls in type(exc).__mro__:
        if cls in table:
            return table[cls]
    return default


def register_error_handlers(app) -> None:
    @app.errorhandler(AppError)
    def handle_app_error(e):
        logger.warning("%s: %s", type(e).__name__, e)
        message = str(e) or _lookup(DEFAULT_MESSAGES, e, DEFAULT_MESSAGE)
        return jsonify({"error": message}), _lookup(STATUS_CODES, e, DEFAULT_STATUS_CODE)

    @app.errorhandler(HTTPException)
    def handle_http_error(e):
        return jsonify({"error": e.description}), e.code

    @app.errorhandler(Exception)
    def handle_unexpected(e):
        logger.exception("Error interno no controlado.")
        return jsonify({"error":"Error interno"}), 500
