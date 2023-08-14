from mongoengine import Document, ReferenceField, BooleanField, DateTimeField, StringField, ListField
from datetime import datetime

from app.models.user import User
from app.models.post import Post


class Comment(Document):
    comment = StringField(required=True, max_length=300)
    likes = ListField(ReferenceField(User), default=list)
    post = ReferenceField(Post, required=True)

    created_by = ReferenceField(User, required=True)
    created_at = DateTimeField(default=datetime.utcnow())
    is_deleted = BooleanField(default=False)

    meta = {"collection": "comment", "indexes": ["created_by"]}

    @property
    def like_count(self):
        return len(self.likes)
