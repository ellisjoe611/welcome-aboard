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

    meta = {
        "collection": "post",
        "indexes": [{"fields": ("created_by", "created_at")}],
    }

    def soft_delete(self):
        if g.user != self.created_by:
            return False
        try:
            self.update(set__is_deleted=True)
            return True
        except OperationError:
            return False

    def add_tag(self, tag_name: str):
        try:
            self.update(push__tags=Tag(name=tag_name, created_by=g.user))
            return True
        except OperationError:
            return False

    def remove_tag(self, tag_name: str):
        pass
