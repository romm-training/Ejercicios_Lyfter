from flask import Flask, jsonify, request

from exceptions import BusinessRuleError, InvalidTransitionError, NotFoundError

_BASE_URL = "/api/v1/cars"

def register_car_routes(app: Flask, car_service) -> None:

    @app.route(f"{_BASE_URL}/", methods=["GET"])
    def get_all_cars():
        cars = car_service.get_all_cars(request.args.to_dict())
        return jsonify(cars), 200

    @app.route(f"{_BASE_URL}/<int:car_id>", methods=["GET"])
    def get_car_by_id(car_id):
        car = car_service.get_car_by_id(car_id)
        return jsonify(car), 200

    @app.route(f"{_BASE_URL}/", methods=["POST"])
    def create_car():
        car_data = request.json
        new_car = car_service.create_car(car_data)

        not_allowed_keys = ["status"]
        required_keys = ["make", "model", "year"]
        
        if any(k in car_data for k in not_allowed_keys):
            raise BusinessRuleError(f"Los campos {not_allowed_keys} no están permitido en esta operación.")

        if not all(k in car_data for k in required_keys):
            raise BusinessRuleError(f"Los campos {required_keys} son requeridos.")
        
        return jsonify(new_car), 201

    @app.route(f"{_BASE_URL}/<int:car_id>", methods=["PUT"])
    def update_car(car_id):
        car_data = request.json
        updated = car_service.update_car(car_id, car_data)
        return jsonify(updated), 200

    @app.route(f"{_BASE_URL}/<int:car_id>", methods=["DELETE"])
    def delete_car(car_id):
        car_service.delete_car(car_id)
        return "", 204
