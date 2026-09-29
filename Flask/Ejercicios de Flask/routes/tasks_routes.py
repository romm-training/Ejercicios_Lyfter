from flask import Flask, jsonify, request

from services import task_service

_URL_PREFIX = "/api/v1/tasks"

def register_task_routes(app: Flask) -> None:

    @app.route(_URL_PREFIX, methods=['GET'])
    def get_tasks():
        tasks, error, code = task_service.get_tasks()
        if error:
            return jsonify({"error": error}), code
        return jsonify(tasks), code

    @app.route(f"{_URL_PREFIX}/<int:task_id>", methods=['GET'])
    def get_task(task_id: int):
        tasks, error, code = task_service.get_task(task_id)
        if error:
            return jsonify({"error": error}), code
        return jsonify(tasks), code

    @app.route(_URL_PREFIX, methods=['POST'])
    def create_task():
        data = request.get_json(silent=True) or {}
        task, error, code = task_service.create_task(data)
        if error:
            return jsonify({"error": error}), code
        return jsonify(task), code

    @app.route(f"{_URL_PREFIX}/<int:task_id>", methods=['PUT'])
    def update_task(task_id):
        data = request.get_json(silent=True) or {}
        task, error, code = task_service.update_task(task_id, data)
        if error:
            return jsonify({"error": error}), code
        return jsonify(task), code

    @app.route(f"{_URL_PREFIX}/<int:task_id>", methods=['DELETE'])
    def delete_task(task_id):
        _, error, code = task_service.delete_task(task_id)
        if error:
            return jsonify({"error": error}), code
        return "", code