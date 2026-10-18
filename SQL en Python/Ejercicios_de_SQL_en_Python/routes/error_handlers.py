import logging
from flask import jsonify
from werkzeug.exceptions import HTTPException
from exceptions import AppError

logger = logging.getLogger(__name__)

def register_error_handlers(app) -> None:
    @app.errorhandler(AppError)
    def handle_app_error(e):
        logger.warning("%s: %s", type(e).__name__, e)
        return jsonify({"error":str(e) or e.message}), e.status_code

    @app.errorhandler(HTTPException)
    def handle_http_error(e):
        return jsonify({"error": e.description}), e.code

    @app.errorhandler(Exception)
    def handle_unexpected(e):
        logger.exception("Error interno no controlado.")
        return jsonify({"error":"Error interno"}), 500

