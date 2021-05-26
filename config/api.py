import logging
import os

from flask import Flask
from flask_cache import Cache
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config import settings
from config.database import db, migration
from src.services.firebase import FirebaseService


def load_application():
    app = Flask(__name__)
    app.config.from_object(settings[os.environ.get("FLASK_ENV", "development")])
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    print("System Config", settings[os.environ.get("FLASK_ENV", "development")])

    firebase = FirebaseService()
    firebase.load_firebase()
    jwt = JWTManager(app)
    # Database ORM Initialization
    db.init_app(app)

    # Database Migrations Initialization
    migration.init_app(app, db)
    app.logger = logging.getLogger('console')
    return app


app = load_application()

cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_KEY_PREFIX': settings[os.environ.get("FLASK_ENV", "development")].CACHE_KEY_PREFIX,
    'CACHE_REDIS_URL': settings[os.environ.get("FLASK_ENV", "development")].REDIS_URL
})
cache.init_app(app)