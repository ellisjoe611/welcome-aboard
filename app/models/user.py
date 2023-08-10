from mongoengine import Document, EmailField, StringField, BooleanField, DateTimeField
from bcrypt import checkpw
from datetime import datetime


class User(Document):
    email = EmailField(required=True, unique=True)
    name = StringField(required=True, max_length=50)
    password = StringField(required=True, min_length=8)
    subscribing = BooleanField(default=False)
    is_master = BooleanField(default=False)

    created_at = DateTimeField(default=datetime.utcnow())
    is_deleted = BooleanField(default=False)

    meta = {"collection": "user", "indexes": ["email", "name"]}

    def check_pw(self, password: str) -> bool:
        return checkpw(password.encode("utf-8"), self.password.encode("utf-8"))
