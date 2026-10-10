from flask import Flask, jsonify, request

_BASE_URL = "/api/v1/cars"

def register_car_routes(app: Flask, car_service) -> None:

    @app.route(f"{_BASE_URL}/", methods=["GET"])
    def get_all_cars():
        try:
            cars = car_service.get_all_cars()
            return jsonify(cars), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route(f"{_BASE_URL}/<int:car_id>", methods=["GET"])
    def get_car_by_id(car_id):
        try:
            car = car_service.get_car_by_id(car_id)
            if car:
                return jsonify(car), 200
            else:
                return jsonify({"error": "Car not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route(f"{_BASE_URL}/", methods=["POST"])
    def create_car():
        try:
            car_data = request.json
            car_service.create_car(car_data)
            return jsonify({"message": "Car created successfully"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route(f"{_BASE_URL}/<int:car_id>", methods=["PUT"])
    def update_car(car_id):
        try:
            car_data = request.json
            updated = car_service.update_car(car_id, car_data)
            if updated:
                return jsonify({"message": "Car updated successfully"}), 200
            else:
                return jsonify({"error": "Car not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route(f"{_BASE_URL}/<int:car_id>", methods=["DELETE"])
    def delete_car(car_id):
        try:
            deleted = car_service.delete_car(car_id)
            if deleted:
                return jsonify({"message": "Car deleted successfully"}), 200
            else:
                return jsonify({"error": "Car not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500