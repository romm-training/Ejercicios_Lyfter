from flask import Flask, jsonify, request

from dtos.user_dto import UserLoginDTO
from services.authentication_service import AuthenticationService
from routes.decorators import AuthenticationGuard
from roles import Role

_BASE_URL = "/api/v1"

def register_authentication_routes(
        app: Flask, 
        authentication_service: AuthenticationService,
        guard: AuthenticationGuard
        ) -> None:
    @app.route(f"{_BASE_URL}/liveness", methods=["GET"])
    @guard.require_role(Role.ADMIN)
    def liveness():
        return jsonify(message="Service is Running")

    @app.route(f"{_BASE_URL}/login", methods=["POST"])
    def login():
        user_data = request.json
        token = authentication_service.login(
            UserLoginDTO.model_validate(user_data)
            )
        return jsonify(token.model_dump(mode="json")), 200
         