from flask import Flask, jsonify, request

from services.product_service import ProductService
from dtos.product_dto import ProductDTO, ProductCreateDTO, ProductUpdateDTO
from routes.decorators import AuthenticationGuard
from roles import Role

_BASE_URL = "/api/v1/products"

def register_product_routes(
        app: Flask, 
        product_service: ProductService,
        guard: AuthenticationGuard
        ) -> None:
    @app.route(f"{_BASE_URL}/", methods=["GET"])
    @guard.require_authentication
    def get_all_products():
        args = request.args
        products = product_service.get_all()
        return jsonify([p.model_dump(mode="json") for p in products]), 200

    @app.route(f"{_BASE_URL}/<int:product_id>", methods=["GET"])
    @guard.require_role(Role.ADMIN)
    def get_product_by_id(product_id: int):
        product = product_service.get_by_id(product_id)
        return jsonify(product.model_dump(mode="json")), 200

    @app.route(f"{_BASE_URL}/", methods=["POST"])
    @guard.require_role(Role.ADMIN)
    def create_product():
        data = request.json
        created = product_service.create(
            ProductCreateDTO.model_validate(data)
            )
        return jsonify(created.model_dump(mode="json")), 201

    @app.route(f"{_BASE_URL}/<int:product_id>", methods=["PUT"])
    @guard.require_role(Role.ADMIN)
    def update_product(product_id: int):
        data = request.json
        updated = product_service.update(
            product_id,
            ProductUpdateDTO.model_validate(data)
            )
        return jsonify(updated.model_dump(mode="json")), 200

    @app.route(f"{_BASE_URL}/<int:product_id>", methods=["DELETE"])
    @guard.require_role(Role.ADMIN)
    def delete_product(product_id: int):
        product_service.delete(product_id)
        return "", 204
        
