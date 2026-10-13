from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<h1>Hello, World!</h1>'

@app.route('/information')
def information():
    return {
        "year": 2024,
        "description": "Esto es un endpoint secundario"
    }

shows_list = [
    {
        "title": "3 Body Problem",
        "genre": "Sci-Fi",
    },
    {
        "title": "Severance",
        "genre": "Thriller",
    },
    {
        "title": "Black Knight",
        "genre": "Sci-Fi",
    }
]

@app.route('/shows')
def shows():
    filtered_shows = shows_list
    genre_filter = request.args.get('genre')
    if genre_filter:
        filtered_shows = list(
            filter(lambda show: show['genre'].lower() == genre_filter.lower(), filtered_shows)
        )

    return { "data": filtered_shows }

@app.route('/echo', methods=['POST'])
def echo():
    request_body = request.json
    return { "request_body": request_body }

comments_list = [
    "Genial video, entendi todo a la perfeccion!",
    "Me encato el intro jajaja"
]

from flask import jsonify

@app.route('/comments', methods=['POST'])
def post_comment():
    comment_content = request.form.get("comment_content")
    if not comment_content:
        return jsonify(message="no empty comments allowed")

    comments_list.append(comment_content)
    return comments_list

users_list = [
    {
        "email": "action.bronson@gmail.com",
        "password": "123@a!",
    }
]

@app.route('/register', methods=['POST'])
def register_user():
    try:
        if "email" not in request.json:
            raise ValueError("Email missing from the boddy")

        if "password" not in request.json:
            raise ValueError("Password missing from the body")

        users_list.append({
            "email": request.json["email"],
            "password": request.json["password"]
        })

        return users_list

    except ValueError as ex:
        return jsonify(message=str(ex)), 400
    except Exception as ex:
        return jsonify(message=str(ex)), 500

@app.route('/view-token')
def view_token():
    token = request.headers.get("token","")
    return token

import json
from flask import Response

@app.route('/hello')
def hello():
    response_body = json.dumps({"msg": "Hello, World!"})
    return Response(response_body, status=200, mimetype='application/json')

from dataclasses import dataclass

@dataclass
class HelloResponse:
    msg: str

@app.route('/hello-dataclass')
def hello_dataclass():
    response = HelloResponse(msg="Hello, World!")
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)