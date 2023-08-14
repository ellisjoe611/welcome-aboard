from typing import Optional
import bcrypt
from mongoengine import Document, EmailField, StringField, BooleanField, DateTimeField, OperationError, ValidationError
from bcrypt import checkpw
from datetime import datetime

from app.api import ApiError


class User(Document):
    email = EmailField(required=True, unique=True)
    name = StringField(required=True, max_length=50)
    password = StringField(required=True)
    subscribing = BooleanField(default=False)
    is_master = BooleanField(default=False)

    created_at = DateTimeField(default=datetime.utcnow())
    updated_at = DateTimeField(default=datetime.utcnow())
    is_deleted = BooleanField(default=False)

    meta = {
        "collection": "user",
        "indexes": [{"fields": ("email", "name")}, {"fields": ("is_master",)}, {"fields": ("is_deleted",)}],
    }

    def check_pw(self, password: str) -> bool:
        return checkpw(password.encode("utf-8"), self.password.encode("utf-8"))

    @classmethod
    def get_user_list(cls, page_no: int, page_size: int, email: Optional[str] = None):
        search_query = dict()
        if email:
            search_query["email"] = email

        try:
            return cls.objects(**search_query).skip((page_no - 1) * page_size).limit(page_size)
        except Exception as e:
            raise ApiError(message=str(e), status_code=500)

    @classmethod
    def get_user_info(cls, email: str):
        try:
            return cls.objects(email=email, is_deleted=False).first()
        except Exception as e:
            raise ApiError(message=str(e), status_code=500)

    def update_user_info(self, change_pw: bool, password: Optional[str] = None, new_password: Optional[str] = None, subscribing: Optional[bool] = None):
        if change_pw is True:
            if not password:
                raise ApiError(message="기존 비밀번호를 입력하세요.", status_code=422)
            if not new_password:
                raise ApiError(message="변경할 비밀번호가 누락되었습니다.", status_code=422)
            if self.check_pw(password=password) is not True:
                raise ApiError(message="비밀번호가 일치하지 않습니다", status_code=401)

            self.password = bcrypt.hashpw(password=new_password.encode(encoding="utf-8"), salt=bcrypt.gensalt()).decode(encoding="utf-8")
        if subscribing is not None:
            self.subscribing = subscribing

        self.updated_at = datetime.utcnow()
        try:
            self.save()
        except (OperationError, ValidationError) as e:
            raise ApiError(message="DB 업데이트 실패", status_code=500)

    def delete_user(self):
        try:
            self.update(is_deleted=True, updated_at=datetime.utcnow())
        except (OperationError, ValidationError):
            raise ApiError(message="DB 업데이트 실패", status_code=500)
