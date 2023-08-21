from typing import List, Any

from bson.objectid import ObjectId
from flask import g
from mongoengine import Document, ReferenceField, BooleanField, DateTimeField, StringField, ListField, IntField
from mongoengine.errors import OperationError, ValidationError, DoesNotExist, MultipleObjectsReturned
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

    meta = {"collection": "comment", "indexes": [{"fields": ("created_at",)}, {"fields": ("post",)}, {"fields": ("is_deleted",)}]}

    @classmethod
    def create_comment(cls, post: Post, content: str) -> None:
        # 댓글 생성
        try:
            cls(post=post, content=content, created_by=g.user).save()
        except OperationError:
            raise ApiError(message="댓글 생성 실패", status_code=500)

    @classmethod
    def get_comment_list(cls, page_no: int, page_size: int, post: Post) -> List[Any]:
        # 댓글 목록 return
        try:
            return cls.objects(post=post, is_deleted=False).skip((page_no - 1) * page_size).limit(page_size).order_by("+created_at")
        except Exception as e:
            raise ApiError(message=str(e), status_code=500)

    @classmethod
    def get_comment_by_id(cls, comment_id: ObjectId):
        # 댓글 불러오기
        try:
            return cls.objects.get(id=comment_id, is_deleted=False)
        except DoesNotExist:
            raise ApiError(message="댓글을 찾을 수 없습니다.", status_code=404)
        except MultipleObjectsReturned:
            raise ApiError(message="조회 도중 에러 발생 (multiple_found_error)", status_code=500)

    def delete_comment(self):
        # 삭제 권한 확인
        if self.created_by != g.user:
            raise ApiError(message="해당 댓글을 삭제할 권한이 없습니다.", status_code=403)

        # 댓글 삭제 진행
        try:
            self.update(set__is_deleted=True, set__updated_at=datetime.utcnow())
        except (OperationError, ValidationError):
            raise ApiError(message="댓글 삭제 실패", status_code=500)

    def add_like(self):
        # 좋아요 여부가 있으면 error
        if g.user in self.likes:
            raise ApiError(message="이미 좋아요를 누른 댓글 입니다.", status_code=409)

        # 좋아요 추가 진행
        try:
            self.update(push__likes=g.user, inc__likes_cnt=1)
        except OperationError:
            raise ApiError(message="좋아요 추가 실패", status_code=500)

    def remove_like(self):
        # 좋아요 여부가 없으면 error
        if g.user not in self.likes:
            raise ApiError(message="좋아요를 누른 댓글이 아닙니다.", status_code=409)

        # 좋아요 취소 진행
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
