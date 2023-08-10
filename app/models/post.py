from mongoengine import Document, ReferenceField, BooleanField, DateTimeField, StringField, ListField, OperationError
from datetime import datetime
from flask import g

from app.models.user import User
from app.models.tag import Tag


class Post(Document):
    title = StringField(required=True, max_length=100)
    content = StringField(required=True, max_length=1000)
    tags = ListField(ReferenceField(Tag), default=list)
    likes = ListField(ReferenceField(User), default=list)

    created_by = ReferenceField(User, required=True)
    created_at = DateTimeField(default=datetime.utcnow())
    updated_at = DateTimeField(default=datetime.utcnow())
    is_deleted = BooleanField(default=False)

    meta = {"collection": "post", "indexes": ["created_by"]}

    def soft_delete(self):
        if g.user != self.created_by:
            return False
        try:
            self.update(is_deleted=True)
            return True
        except OperationError as err:
            print(str(err))
            return False
