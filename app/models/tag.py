from datetime import datetime
from flask import g
from typing import Optional

from mongoengine import Document, StringField, ReferenceField, DateTimeField, BooleanField, OperationError, ValidationError

from app.api import ApiError
from app.models.user import User


class Tag(Document):
    name = StringField(required=True, unique=True, min_length=2, max_length=10)

    created_by = ReferenceField(User, required=True)
    created_at = DateTimeField(default=datetime.utcnow())
    is_deleted = BooleanField(default=False)

    meta = {"collection": "tag", "indexes": [{"fields": ("name",)}, {"fields": ("is_deleted",)}]}

    @classmethod
    def create_tag(cls, name: str):
        if cls.objects(name=name).count() > 0:
            raise ApiError(message="이미 존재하거나 등록되었던 Tag가 있습니다.", status_code=409)

        try:
            current_user = User.objects(email=g.user.email, is_deleted=False).first()
            if not current_user:
                raise ApiError(message="사용자 조회 실패", status_code=500)
            new_tag = cls(name=name, created_by=current_user)
            new_tag.save()
        except (OperationError, ValidationError) as err:
            raise ApiError(message="DB 업데이트 실패", status_code=500)

    @classmethod
    def list_tag(cls, page_no: int, page_size: int, name: Optional[str] = None):
        search_query = dict()
        if name:
            search_query["name"] = name

        try:
            return cls.objects(**search_query).skip((page_no - 1) * page_size).limit(page_size)
        except Exception as e:
            raise ApiError(message=str(e), status_code=500)

    def delete_tag(self):
        try:
            self.update(is_deleted=True, updated_at=datetime.utcnow())
        except (OperationError, ValidationError):
            raise ApiError(message="DB 업데이트 실패", status_code=500)
