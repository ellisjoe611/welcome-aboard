from flask import Flask
from flask_cors import CORS
import mongoengine

from app.config import LocalhostConfig, Config
from app.views import register_api


def create_app(is_localhost: bool = False) -> Flask:
    app = Flask(__name__)

    # MongoDB Connection
    try:
        if is_localhost is True:
            app.config.from_object(LocalhostConfig)
            mongoengine.connect(db=LocalhostConfig.MONGODB_DB, host=LocalhostConfig.MONGODB_URI)
        else:
            app.config.from_object(Config)
            mongoengine.connect(db=Config.MONGODB_DB, host=Config.MONGODB_URI)
    except Exception as db_err:
        print(f"[ERROR] Something went wrong with MongoDB connection\n{str(db_err)}")

    # CORS apply
    CORS(app)

    # register api router
    register_api(app)

    # health check
    @app.route("/")
    def health_check():
        return "", 200

    return app
