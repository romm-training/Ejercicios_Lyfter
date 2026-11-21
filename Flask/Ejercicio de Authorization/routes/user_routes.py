from flask import Flask, jsonify, request, g

from dtos.user_dto import UserCreateDTO, UserUpdateDTO
from services.user_service import UserService
from routes.decorators import AuthenticationGuard
from roles import Role

_BASE_URL = "/api/v1/users"

def register_user_routes(
        app: Flask, 
        user_service: UserService,
        guard: AuthenticationGuard
    ) -> None:
    @app.route(f"{_BASE_URL}", methods=["GET"])
    @guard.require_role(Role.ADMIN)
    def get_all_users():
        args = request.args.to_dict()
        users = user_service.get_all()
        return jsonify([u.model_dump(mode="json") for u in users]), 200

    @app.route(f"{_BASE_URL}/<int:user_id>", methods=["GET"])
    @guard.require_role(Role.ADMIN)
    def get_user_by_id(user_id: int):
        user = user_service.get_by_id(user_id)
        return jsonify(user.model_dump(mode="json")), 200

    @app.route(f"{_BASE_URL}", methods=["POST"])
    def create_user():
        user_data = request.json
        created_user = user_service.create(
            UserCreateDTO.model_validate(user_data)
            )
        return jsonify(created_user.model_dump(mode="json")), 201

    @app.route(f"{_BASE_URL}/<int:user_id>", methods=["PUT"])
    @guard.require_authentication
    def update_user(user_id: int):
        user_data = request.json
        updated_user = user_service.update(
            user_id, 
            UserUpdateDTO.model_validate(user_data)
            )
        return jsonify(updated_user.model_dump(mode="json")), 200

    @app.route(f"{_BASE_URL}/<int:user_id>", methods=["DELETE"])
    @guard.require_role(Role.ADMIN)
    def delete_user(user_id: int):
        user_service.delete(user_id)
        return "", 204

    @app.route(f"{_BASE_URL}/me", methods=["GET"])
    @guard.require_authentication
    def me():
        user = user_service.get_by_id(int(g.current_user["sub"]))
        return jsonify(user.model_dump(mode="json")), 200
        
