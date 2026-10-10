from flask import Flask, jsonify, request

_BASE_URL = "/api/v1/rentals"

def register_car_rental_routes(app, car_rental_service) -> None:
    @app.route(f"{_BASE_URL}/", methods=["GET"])
    def get_all_rentals():
        try:
            rentals = car_rental_service.get_all_rentals()
            return jsonify(rentals), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route(f"{_BASE_URL}/<int:rental_id>", methods=["GET"])
    def get_rental_by_id(rental_id):
        try:
            rental = car_rental_service.get_rental_by_id(rental_id)
            if rental:
                return jsonify(rental), 200
            else:
                return jsonify({"error": "Rental not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route(f"{_BASE_URL}/", methods=["POST"])
    def create_rental():
        try:
            rental_data = request.json
            car_rental_service.create_rental(rental_data)
            return jsonify({"message": "Rental created successfully"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route(f"{_BASE_URL}/<int:rental_id>", methods=["PUT"])
    def update_rental(rental_id):
        try:
            rental_data = request.json
            updated = car_rental_service.update_rental(rental_id, rental_data)
            if updated:
                return jsonify({"message": "Rental updated successfully"}), 200
            else:
                return jsonify({"error": "Rental not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route(f"{_BASE_URL}/<int:rental_id>", methods=["DELETE"])
    def delete_rental(rental_id):
        try:
            deleted = car_rental_service.delete_rental(rental_id)
            if deleted:
                return jsonify({"message": "Rental deleted successfully"}), 200
            else:
                return jsonify({"error": "Rental not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500