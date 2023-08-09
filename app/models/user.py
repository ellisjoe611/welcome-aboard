from mongoengine import Document, EmailField, StringField, BooleanField, DateTimeField
from bcrypt import checkpw
from datetime import datetime
from flask import current_app
import jwt


class User(Document):
    email = EmailField(required=True, unique=True)
    name = StringField(required=True, max_length=50)
    password = StringField(required=True, min_length=8)
    subscribing = BooleanField(default=False)
    is_master = BooleanField(default=False)

    created_at = DateTimeField(default=datetime.utcnow())
    is_deleted = BooleanField(default=False)

    meta = {"indexes": ["email", "name"]}

    def check_pw(self, password: str) -> bool:
        return checkpw(password.encode("utf-8"), self.password.encode("utf-8"))

    def get_new_token(self):
        return jwt.encode(payload=dict(email=self.email, is_master=self.is_master), key=current_app.config["TOKEN_KEY"], algorithm=current_app.config["ALGORITHM"])
