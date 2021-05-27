import json
import os

from faker import Faker
from flask_testing import TestCase

from config.api import app
from config.database import db
from src.services.firebase import FirebaseService
from src.services.roles import RolesService
from src.services.store import StoreService
from src.services.user import UserService
from src.utils.enums import RolesTypes
from src.utils.firebase_utils import create_firebase_user, setup_firebase_client, login_user, is_json_key_present


class BaseTestCase(TestCase):
    """A base test case."""

    fake = Faker()
    userService = UserService()
    roleService = RolesService()
    storeService = StoreService()
    TESTING = True
    firebase_owner_user = "test+owner@user.com"
    firebase_support_user = "test+support@user.com"
    firebase_account_user = "test+account@user.com"
    firebase_global_password = "password!0101"
    firebase_owner_object = None
    firebase_support_object = None
    firebase_accounts_object = None
    firebase_client_object = None
    firebaseService = FirebaseService()

    def create_app(self):
        # app.config.from_object('config.TestConfig')
        print(os.environ.get("FLASK_ENV", "development"))
        self.firebase_client_object = setup_firebase_client()
        app.app_context().push()
        return app

    def setUp(self):
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()
        db.session.commit()
        self.roleService.insert_roles()
        print(self.roleService.get_all_roles())
        self.init_unit_data()
        Faker.seed(0)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def login_user(self, email, password):
        user = login_user(self.firebase_owner_user, self.firebase_global_password)
        self.assertFalse(is_json_key_present(user, 'error'))
        token = user['idToken']
        self.assertIsNotNone(token)
        self.assertNotEqual(token, '')
        return {
            'idToken': token,
            'uid': user['localId'],
            'display_name': user['displayName']
        }

    def init_unit_data(self):
        self.setup_owner_user()
        self.setup_account_user()
        self.setup_support_user()

    def setup_owner_user(self):
        self.firebase_owner_object = create_firebase_user(self.firebase_owner_user, self.firebase_global_password)
        self.assertIsNotNone(self.firebase_owner_object)
        if self.firebase_owner_object is not None:
            self.assertNotEqual(self.firebase_owner_object.uid, '')
        roles = self.roleService.get_roles([RolesTypes.Owner.value])
        self.userService.sync_firebase_user(self.firebase_owner_object.uid, roles, True)

    def setup_support_user(self):
        self.firebase_support_object = create_firebase_user(self.firebase_support_user, self.firebase_global_password)
        self.assertIsNotNone(self.firebase_support_object)
        if self.firebase_support_object is not None:
            self.assertNotEqual(self.firebase_support_object.uid, '')
        roles = self.roleService.get_roles([RolesTypes.Support.value])
        self.userService.sync_firebase_user(self.firebase_owner_object.uid, roles, True)

    def setup_account_user(self):
        self.firebase_accounts_object = create_firebase_user(self.firebase_account_user, self.firebase_global_password)
        self.assertIsNotNone(self.firebase_accounts_object)
        if self.firebase_accounts_object is not None:
            self.assertNotEqual(self.firebase_accounts_object.uid, '')
        roles = self.roleService.get_roles([RolesTypes.Accounts.value])
        self.userService.sync_firebase_user(self.firebase_owner_object.uid, roles, True)

    def create_store_user(self, store_code,roles):
        self.firebase_accounts_object = create_firebase_user(self.firebase_account_user, self.firebase_global_password)
        self.assertIsNotNone(self.firebase_accounts_object)
        if self.firebase_accounts_object is not None:
            self.assertNotEqual(self.firebase_accounts_object.uid, '')
        roles = self.roleService.get_roles(roles)
        self.userService.sync_firebase_user(self.firebase_owner_object.uid, roles, False, store_code)

    def request_get(self, url , token):
        headers = {'Content-Type': 'application/json', 'Authorization': token}
        return self.client.get(
            url,
            headers=headers
        )

    def request_put(self, url, token, data={}):
        headers = {'Content-Type': 'application/json', 'Authorization': token}
        return self.client.put(
            url,
            body=json.dumps(data),
            headers=headers
        )
    def request_post(self, url, token, data={}):
        headers = {'Content-Type': 'application/json', 'Authorization': token}
        return self.client.post(
            url,
            body=json.dumps(data),
            headers=headers
        )
    def request_delete(self, url, token):
        headers = {'Content-Type': 'application/json', 'Authorization': token}
        return self.client.delete(
            url,
            headers=headers
        )

class Struct:
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
               setattr(self, a, [Struct(x) if isinstance(x, dict) else x for x in b])
            else:
               setattr(self, a, Struct(b) if isinstance(b, dict) else b)