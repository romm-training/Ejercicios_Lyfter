from flask import Flask, jsonify

_BASE_URL = "/api/v1/health"

def register_health_routes(app: Flask, health_service) -> None:
    @app.route(f"{_BASE_URL}/", methods=["GET"])
    def health():
        result = health_service.validate_system_health()
        return jsonify(result), 200 if result["healthy"] else 503