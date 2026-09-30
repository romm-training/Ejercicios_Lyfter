from flask import Flask
import logging

from routes.tasks_routes import register_task_routes

def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

configure_logging()

app = Flask(__name__)

register_task_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
