from flask import Flask

from routes.tasks_routes import register_task_routes

app = Flask(__name__)

register_task_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
