from mongoengine import Document, ReferenceField, BooleanField, DateTimeField, StringField, ListField
from datetime import datetime
from flask import g, current_app

from app.models.user import User
from app.models.comment import Comment


class Post(Document):
    title = StringField(required=True, max_length=100)
    content = StringField(required=True)
    tags = ListField(StringField(), default=list)
    likes = ListField(ReferenceField(User), default=list)

    created_by = ReferenceField(User, required=True)
    created_at = DateTimeField(default=datetime.utcnow())
    is_deleted = BooleanField(default=False)

    @property
    def count_likes(self) -> int:
        return len(self.likes)

    @property
    def list_comments(self):
        return Comment.objects(post=self)

    @property
    def check_liked(self) -> bool:
        return User.objects(email=g.email) in self.likes

    @property
    def writer(self):
        return self.created_by
