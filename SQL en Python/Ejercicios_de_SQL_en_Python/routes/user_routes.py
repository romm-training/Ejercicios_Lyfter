from flask import Flask, jsonify, request

_BASE_URL = "/api/v1/users"

def register_user_routes(app: Flask, user_service) -> None:

    @app.route(f"{_BASE_URL}/", methods=["GET"])
    def get_all_users():
        try:
            users = user_service.get_all_users()
            return jsonify(users), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route(f"{_BASE_URL}/<int:user_id>", methods=["GET"])
    def get_user_by_id(user_id):
        try:
            user = user_service.get_user_by_id(user_id)
            if user:
                return jsonify(user), 200
            else:
                return jsonify({"error": "User not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route(f"{_BASE_URL}/", methods=["POST"])
    def create_user():
        try:
            user_data = request.json
            user_service.create_user(user_data)
            return jsonify({"message": "User created successfully"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route(f"{_BASE_URL}/<int:user_id>", methods=["PUT"])
    def update_user(user_id):
        try:
            user_data = request.json
            updated = user_service.update_user(user_id, user_data)
            if updated:
                return jsonify({"message": "User updated successfully"}), 200
            else:
                return jsonify({"error": "User not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route(f"{_BASE_URL}/<int:user_id>", methods=["DELETE"])
    def delete_user(user_id):
        try:
            deleted = user_service.delete_user(user_id)
            if deleted:
                return jsonify({"message": "User deleted successfully"}), 200
            else:
                return jsonify({"error": "User not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500