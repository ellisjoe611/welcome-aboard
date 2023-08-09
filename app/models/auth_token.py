from mongoengine import Document, StringField
from flask import current_app
import jwt


class AuthToken(Document):
    token = StringField(required=True)

    meta = {"indexes": ["token"]}

    @classmethod
    def get_new_token(cls, email: str, is_master: bool):
        return cls(token=jwt.encode(payload={"email": email, "is_master": is_master}, key=current_app.config["TOKEN_KEY"], algorithm=current_app.config["ALGORITHM"]))
