from flask import Flask, jsonify, request

from exceptions import BusinessRuleError, InvalidTransitionError, NotFoundError

_BASE_URL = "/api/v1/users"

def register_user_routes(app: Flask, user_service) -> None:

    @app.route(f"{_BASE_URL}/", methods=["GET"])
    def get_all_users():
        users = user_service.get_all_users(request.args.to_dict())
        return jsonify(users), 200

    @app.route(f"{_BASE_URL}/<int:user_id>", methods=["GET"])
    def get_user_by_id(user_id):
        user = user_service.get_user_by_id(user_id)
        return jsonify(user), 200

    @app.route(f"{_BASE_URL}/", methods=["POST"])
    def create_user():
        user_data = request.json
        created_user = user_service.create_user(user_data)
        return jsonify(created_user), 201

    @app.route(f"{_BASE_URL}/<int:user_id>", methods=["PUT"])
    def update_user(user_id):
        user_data = request.json
        updated = user_service.update_user(user_id, user_data)
        return jsonify(updated), 200

    @app.route(f"{_BASE_URL}/<int:user_id>", methods=["DELETE"])
    def delete_user(user_id):
        user_service.delete_user(user_id)
        return "", 204
