from flask import Flask, jsonify, request
from exceptions import BusinessRuleError, InvalidTransitionError, NotFoundError

_BASE_URL = "/api/v1/rentals"

def register_car_rental_routes(app, car_rental_service) -> None:
    @app.route(f"{_BASE_URL}/", methods=["GET"])
    def get_all_rentals():
        rentals = car_rental_service.get_all_rentals(request.args.to_dict())
        return jsonify(rentals), 200

    @app.route(f"{_BASE_URL}/<int:rental_id>", methods=["GET"])
    def get_rental_by_id(rental_id):
        rental = car_rental_service.get_rental_by_id(rental_id)
        return jsonify(rental), 200

    @app.route(f"{_BASE_URL}/", methods=["POST"])
    def create_rental():
        rental_data = request.json
        not_allowed_keys = ["rental_date_at"]
        required_keys = ["car_id", "user_id", "return_date_at", "status"]
        
        if any(k in rental_data for k in not_allowed_keys):
            raise BusinessRuleError("El campo 'rental_date_at' no está permitido en esta operación.")

        if not all(k in rental_data for k in required_keys):
            raise BusinessRuleError("Los campos 'car_id', 'user_id', 'return_date_at' y 'status' son requeridos.")
        
        result = car_rental_service.create_rental(rental_data)
        return jsonify(result), 201

    @app.route(f"{_BASE_URL}/<int:rental_id>", methods=["PUT"])
    def update_rental(rental_id):
        rental_data = request.json
        not_allowed_keys = ["car_id", "user_id", "rental_date_at"]
        required_keys = ["status"]

        if any(k in rental_data for k in not_allowed_keys):
            raise BusinessRuleError("Los campos 'car_id', 'user_id' y 'rental_date_at' no están permitidos en esta operación.")
        if not all(k in rental_data for k in required_keys):
            raise BusinessRuleError("El campo 'status' es requerido.")
        
        updated = car_rental_service.update_rental(rental_id, rental_data)
        return jsonify(updated), 200

    @app.route(f"{_BASE_URL}/<int:rental_id>", methods=["DELETE"])
    def delete_rental(rental_id):
        car_rental_service.delete_rental(rental_id)
        return "", 204
