from flask import Flask, jsonify, request
from exceptions import BusinessRuleError, InvalidTransitionError, NotFoundError

_BASE_URL = "/api/v1/rentals"

def register_car_rental_routes(app, car_rental_service) -> None:
    @app.route(f"{_BASE_URL}/", methods=["GET"])
    def get_all_rentals():
        try:
            rentals = car_rental_service.get_all_rentals(request.args.to_dict())
            return jsonify(rentals), 200
        except BusinessRuleError as e:
            #logging str(e)
            return jsonify({"error": f"Error al obtener los registros: {e}"}), 422
        except InvalidTransitionError as e:
            #logging str(e)
            return jsonify({"error": "Error al obtener los registros."}), 409
        except NotFoundError as e:
            #logging str(e)
            return jsonify([]), 200
        except Exception as e:
            #logging str(e)
            return jsonify({"error": "Excepción al obtener los registros."}), 500

    @app.route(f"{_BASE_URL}/<int:rental_id>", methods=["GET"])
    def get_rental_by_id(rental_id):
        try:
            rental = car_rental_service.get_rental_by_id(rental_id)
            return jsonify(rental), 200
        except BusinessRuleError as e:
            #logging str(e)
            return jsonify({"error": f"Error al obtener el registro: {e}"}), 422
        except InvalidTransitionError as e:
            #logging str(e)
            return jsonify({"error": "Error al obtener el registro."}), 409
        except NotFoundError as e:
            #logging str(e)
            return jsonify({"error": "Registro no encontrado."}), 404
        except Exception as e:
            #logging str(e)
            return jsonify({"error": "Excepción al obtener el registro."}), 500

    @app.route(f"{_BASE_URL}/", methods=["POST"])
    def create_rental():
        try:
            rental_data = request.json
            result = car_rental_service.create_rental(rental_data)
            return jsonify(result), 201
        except BusinessRuleError as e:
            #logging str(e)
            return jsonify({"error": f"Error al crear el registro: {e}"}), 422
        except InvalidTransitionError as e:
            #logging str(e)
            return jsonify({"error": "Error al crear el registro."}), 409
        except NotFoundError as e:
            #logging str(e)
            return jsonify({"error": "Registro no encontrado."}), 404
        except Exception as e:
            #logging str(e)
            return jsonify({"error": "Excepción al crear el registro."}), 500

    @app.route(f"{_BASE_URL}/<int:rental_id>", methods=["PUT"])
    def update_rental(rental_id):
        try:
            rental_data = request.json
            if rental_data["car_id"] or rental_data["user_id"] or rental_data["rental_date_at"]:
                raise BusinessRuleError("Los campos 'car_id', 'user_id' y 'rental_date_at' no están permitidos en esta operación.")
            updated = car_rental_service.update_rental(rental_id, rental_data)
            return jsonify(updated), 200
        except BusinessRuleError as e:
            #logging str(e)
            return jsonify({"error":f"Error al actualizar el registro: {e}"}), 422
        except InvalidTransitionError as e:
            #logging str(e)
            return jsonify({"error": "Error al actualizar el registro."}), 409
        except NotFoundError as e:
            #logging str(e)
            return jsonify({"error": "Registro no encontrado."}), 404
        except Exception as e:
            #logging str(e)
            return jsonify({"error": "Excepción al actualizar el registro."}), 500

    @app.route(f"{_BASE_URL}/<int:rental_id>", methods=["DELETE"])
    def delete_rental(rental_id):
        try:
            car_rental_service.delete_rental(rental_id)
            return "", 204
        except BusinessRuleError as e:
            #logging str(e)
            return jsonify({"error": f"Error al eliminar el registro: {e}"}), 422
        except InvalidTransitionError as e:
            #logging str(e)
            return jsonify({"error": "Error al eliminar el registro."}), 409
        except NotFoundError as e:
            #logging str(e)
            return jsonify({"error": "Registro no encontrado."}), 404
        except Exception as e:
            #logging str(e)
            return jsonify({"error": "Excepción al eliminar el registro."}), 500