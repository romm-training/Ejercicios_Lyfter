from flask import Flask, jsonify

_BASE_URL = "/api/v1/backup"

def register_backup_routes(app: Flask, backup_service) -> None:
    @app.route(f"{_BASE_URL}/", methods=["POST"])
    def backup():
        result = backup_service.execute_backup()
        return jsonify(result), 200
