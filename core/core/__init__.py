from flask import Flask
from dotenv import load_dotenv
from core.api import bp

load_dotenv()

def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return "Access the API via /api"

    @app.route("/health/")
    def health_index():
        return "ok"

    app.register_blueprint(bp)

    return app
