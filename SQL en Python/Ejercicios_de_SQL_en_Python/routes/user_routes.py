from flask import Flask, jsonify, request

from exceptions import BusinessRuleError, InvalidTransitionError, NotFoundError

_BASE_URL = "/api/v1/users"

def register_user_routes(app: Flask, user_service) -> None:

    @app.route(f"{_BASE_URL}/", methods=["GET"])
    def get_all_users():
        try:
            users = user_service.get_all_users(request.args.to_dict())
            return jsonify(users), 200
        except BusinessRuleError as e:
            #logging str(e)
            return jsonify({"error": f"Error al obtener los registros: {e}."}), 422
        except InvalidTransitionError as e:
            #logging str(e)
            return jsonify({"error": "Error al obtener los registros."}), 409
        except NotFoundError as e:
            #logging str(e)
            return jsonify([]), 200
        except Exception as e:
            #logging str(e)
            return jsonify({"error": "Excepción al obtener los registros."}), 500

    @app.route(f"{_BASE_URL}/<int:user_id>", methods=["GET"])
    def get_user_by_id(user_id):
        try:
            user = user_service.get_user_by_id(user_id)
            return jsonify(user), 200
        except BusinessRuleError as e:
            #logging str(e)
            return jsonify({"error": f"Error al obtener el registro: {e}."}), 422
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
    def create_user():
        try:
            user_data = request.json
            created_user = user_service.create_user(user_data)
            return jsonify(created_user), 201
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

    @app.route(f"{_BASE_URL}/<int:user_id>", methods=["PUT"])
    def update_user(user_id):
        try:
            user_data = request.json
            updated = user_service.update_user(user_id, user_data)
            return jsonify(updated), 200
        except BusinessRuleError as e:
            #logging str(e)
            return jsonify({"error": f"Error al actualizar el registro: {e}."}), 422
        except InvalidTransitionError as e:
            #logging str(e)
            return jsonify({"error": "Error al actualizar el registro."}), 409
        except NotFoundError as e:
            #logging str(e)
            return jsonify({"error": "Registro no encontrado."}), 404
        except Exception as e:
            #logging str(e)
            return jsonify({"error": "Excepción al actualizar el registro."}), 500

    @app.route(f"{_BASE_URL}/<int:user_id>", methods=["DELETE"])
    def delete_user(user_id):
        try:
            user_service.delete_user(user_id)
            return "", 204
        except BusinessRuleError as e:
            #logging str(e)
            return jsonify({"error": f"Error al eliminar el registro: {e}."}), 422
        except InvalidTransitionError as e:
            #logging str(e)
            return jsonify({"error": "Error al eliminar el registro."}), 409
        except NotFoundError as e:
            #logging str(e)
            return jsonify({"error": "Registro no encontrado."}), 404
        except Exception as e:
            #logging str(e)
            return jsonify({"error": "Excepción al eliminar el registro."}), 500