from datetime import datetime
from flask import g
from typing import Optional

from mongoengine import Document, StringField, ReferenceField, DateTimeField, OperationError, ValidationError, DoesNotExist, MultipleObjectsReturned

from app.api import ApiError
from app.models.user import User


class Category(Document):
    name = StringField(required=True, unique=True, min_length=2, max_length=10)

    created_by = ReferenceField(User, required=True)
    created_at = DateTimeField(default=datetime.utcnow())

    meta = {"collection": "category", "indexes": [{"fields": ("name",)}]}

    @classmethod
    def create_category(cls, name: str):
        if cls.objects(name=name).count() > 0:
            raise ApiError(message="이미 존재하거나 등록되었던 카테고리가 있습니다.", status_code=409)

        try:
            cls(name=name, created_by=g.user).save()
        except (OperationError, ValidationError):
            raise ApiError(message="DB 업데이트 실패", status_code=500)

    @classmethod
    def get_category_list(cls, name: Optional[str] = None):
        search_query = dict()
        if name:
            search_query["name__icontains"] = name

        try:
            return cls.objects(**search_query).exclude("created_at").order_by("+name")
        except Exception as e:
            raise ApiError(message=str(e), status_code=500)

    @classmethod
    def get_category_by_name(cls, name: str):
        try:
            return cls.objects.get(name=name)
        except DoesNotExist:
            raise ApiError(message=f"Category '{name}' not found", status_code=404)
        except MultipleObjectsReturned:
            raise ApiError(message="Duplicate categories found", status_code=500)

    def delete_category(self):
        try:
            self.delete()
        except (OperationError, ValidationError):
            raise ApiError(message="카테고리 삭제 실패", status_code=500)
