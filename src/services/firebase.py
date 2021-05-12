import os

import firebase_admin
from firebase_admin import credentials
from src.utils.singleton import  singleton
import config


@singleton
class FirebaseService:
    def load_firebase(self):
        cred = credentials.Certificate(
            config.settings[os.environ.get("FLASK_ENV", "development")].GOOGLE_APPLICATION_CREDENTIALS)
        firebase_admin.initialize_app(cred)
        pass
