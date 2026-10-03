from flask import Flask, jsonify, request

from services import task_service
from utils.http_errors import HTTP_CODES


_URL_PREFIX = "/api/v1/tasks"

def register_task_routes(app: Flask) -> None:

    def _is_error_response_code(code) -> bool:
        return code >= HTTP_CODES.E300

    @app.route(_URL_PREFIX, methods=['GET'])
    def get_tasks():
        status_filter = request.args.get("status")
        tasks, message, code = task_service.get_tasks(status_filter)
        if _is_error_response_code(code):
            return jsonify({"error": message}), code
        return jsonify(tasks), code

    @app.route(f"{_URL_PREFIX}/<int:task_id>", methods=['GET'])
    def get_task(task_id: int):
        tasks, message, code = task_service.get_task(task_id)
        if _is_error_response_code(code):
            return jsonify({"error": message}), code
        return jsonify(tasks), code

    @app.route(_URL_PREFIX, methods=['POST'])
    def create_task():
        data = request.get_json(silent=True) or {}
        task, message, code = task_service.create_task(data)
        if _is_error_response_code(code):
            return jsonify({"error": message}), code
        return jsonify(task), code

    @app.route(f"{_URL_PREFIX}/<int:task_id>", methods=['PUT'])
    def update_task(task_id):
        data = request.get_json(silent=True) or {}
        task, message, code = task_service.update_task(task_id, data)
        if _is_error_response_code(code):
            return jsonify({"error": message}), code
        return jsonify(task), code

    @app.route(f"{_URL_PREFIX}/<int:task_id>", methods=['DELETE'])
    def delete_task(task_id):
        _, message, code = task_service.delete_task(task_id)
        if _is_error_response_code(code):
            return jsonify({"error": message}), code
        return "", code