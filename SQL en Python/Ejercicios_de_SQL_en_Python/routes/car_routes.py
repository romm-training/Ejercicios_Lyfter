from flask import Flask, jsonify, request

from exceptions import BusinessRuleError, InvalidTransitionError, NotFoundError

_BASE_URL = "/api/v1/cars"

def register_car_routes(app: Flask, car_service) -> None:

    @app.route(f"{_BASE_URL}/", methods=["GET"])
    def get_all_cars():
        try:
            cars = car_service.get_all_cars(request.args.to_dict())
            return jsonify(cars), 200
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

    @app.route(f"{_BASE_URL}/<int:car_id>", methods=["GET"])
    def get_car_by_id(car_id):
        try:
            car = car_service.get_car_by_id(car_id)
            return jsonify(car), 200
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
    def create_car():
        try:
            car_data = request.json
            new_car = car_service.create_car(car_data)
            return jsonify(new_car), 201
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

    @app.route(f"{_BASE_URL}/<int:car_id>", methods=["PUT"])
    def update_car(car_id):
        try:
            car_data = request.json
            updated = car_service.update_car(car_id, car_data)
            return jsonify(updated), 200
        except BusinessRuleError as e:
            #logging str(e)
            return jsonify({"error": f"Error al actualizar el registro: {e}"}), 422
        except InvalidTransitionError as e:
            #logging str(e)
            return jsonify({"error": "Error al actualizar el registro."}), 409
        except NotFoundError as e:
            #logging str(e)
            return jsonify({"error": "Registro no encontrado."}), 404
        except Exception as e:
            #logging str(e)
            return jsonify({"error": "Excepción al actualizar el registro."}), 500

    @app.route(f"{_BASE_URL}/<int:car_id>", methods=["DELETE"])
    def delete_car(car_id):
        try:
            car_service.delete_car(car_id)
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