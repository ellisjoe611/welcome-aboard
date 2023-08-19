from bson.objectid import ObjectId
from flask import g
from mongoengine import Document, ReferenceField, BooleanField, DateTimeField, StringField, ListField, IntField, OperationError
from datetime import datetime

from app.api import ApiError
from app.models.user import User
from app.models.post import Post


class Comment(Document):
    post = ReferenceField(Post, required=True)
    content = StringField(required=True, max_length=300)
    likes = ListField(ReferenceField(User), default=list)
    likes_cnt = IntField(default=0)

    created_by = ReferenceField(User, required=True)
    created_at = DateTimeField(default=datetime.utcnow())
    updated_at = DateTimeField(default=datetime.utcnow())
    is_deleted = BooleanField(default=False)

    meta = {"collection": "comment", "indexes": [{"fields": ("created_at",)}, {"fields": ("is_deleted",)}]}

    def add_like(self):
        try:
            self.update(push__likes=g.user, inc__likes_cnt=1)
        except OperationError:
            raise ApiError(message="좋아요 추가 실패", status_code=500)

    def remove_like(self):
        try:
            self.update(pull__likes=g.user, dec__likes_cnt=1)
        except OperationError:
            raise ApiError(message="좋아요 철회 실패", status_code=500)


class ReComment(Document):
    parent_comment = ReferenceField(Comment, required=True)
    content = StringField(required=True, max_length=300)
    likes = ListField(ReferenceField(User), default=list)
    likes_cnt = IntField(default=0)

    created_by = ReferenceField(User, required=True)
    created_at = DateTimeField(default=datetime.utcnow())
    updated_at = DateTimeField(default=datetime.utcnow())
    is_deleted = BooleanField(default=False)

    meta = {"collection": "re_comment", "indexes": [{"fields": ("created_at",)}, {"fields": ("is_deleted",)}]}

    def add_like(self):
        try:
            self.update(push__likes=g.user, inc__likes_cnt=1)
        except OperationError:
            raise ApiError(message="좋아요 추가 실패", status_code=500)

    def remove_like(self):
        try:
            self.update(pull__likes=g.user, dec__likes_cnt=1)
        except OperationError:
            raise ApiError(message="좋아요 철회 실패", status_code=500)

    @classmethod
    def add_re_comment(cls, parent_comment_id_str: str, content: str):
        parent_comment = Comment.objects(id=ObjectId(parent_comment_id_str), is_deleted=False).first()
        if not parent_comment:
            raise ApiError(message="상위 댓글을 찾지 못했습니다.", status_code=404)

        try:
            cls(parent_comment=parent_comment, content=content, created_by=g.user).save()
        except OperationError:
            raise ApiError(message="대댓글 추가 실패", status_code=500)
