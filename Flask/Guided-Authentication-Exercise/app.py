from flask import Flask, request, jsonify

from user_repository import user_repository
from jwt_manager import JWTManager

ACCESS_TOKEN_EXPIRATION = 60 * 15 #15 minutos
REFRESH_TOKEN_EXPIRATION = 60 * 60 * 24 * 7 #7 dias

app = Flask("user-service")

jwt_manager = JWTManager(
    secret="trespatitos",
    algorithm="HS256",
    access_expiration=ACCESS_TOKEN_EXPIRATION,
    refresh_expiration=REFRESH_TOKEN_EXPIRATION
)

@app.route("/liveness")
def liveness():
    return jsonify(message="Service is running")

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username is None or password is None:
        return jsonify(error="Username and password are required"), 400

    new_user = user_repository.create(username, password)
    access_token, refresh_token = jwt_manager.generate_tokens(new_user.id)

    return jsonify(access_token=access_token, refresh_token=refresh_token), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username is None or password is None:
        return jsonify(error="Username and password are required"), 400

    user = user_repository.get_by_credentials(username, password)
    if user is None:
        return jsonify(error="Invalid username or password"), 401

    access_token, refresh_token = jwt_manager.generate_tokens(user.id)
    return jsonify(access_token=access_token, refresh_token=refresh_token)

@app.route("/me")
def me():
    token = request.headers.get("Authorization")
    if token is None:
        return jsonify(error="Missing Authorization header"), 401

    token = token.replace("Bearer ", "")
    decoded = jwt_manager.decode_token(token, "access")
    if decoded is None:
        return jsonify(error="Invalid or expired access token"), 401

    user = user_repository.get_by_id(decoded["id"])
    if user is None:
        return jsonify(error="User not found"), 404

    return jsonify(id=user.id, username=user.username)

@app.route("/refresh", methods=["POST"])
def refresh():
    data = request.get_json()
    refresh_token = data.get("refresh_token")

    if refresh_token is None:
        return jsonify(error="Refresh token is required"), 400

    decoded = jwt_manager.decode_token(refresh_token, "refresh")
    if decoded is None:
        return jsonify(error="Invalid or expired refresh token"), 401

    user = user_repository.get_by_id(decoded["id"])
    if user is None:
        return jsonify(error="User not found"), 404

    access_token, new_refresh_token = jwt_manager.generate_tokens(user.id)
    return jsonify(access_token=access_token, refresh_token=new_refresh_token)

if __name__ == "__main__":
    app.run(debug=True)