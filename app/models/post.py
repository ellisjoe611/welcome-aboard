from typing import Optional, List
from bson.objectid import ObjectId
from mongoengine import Document, ReferenceField, BooleanField, DateTimeField, StringField, ListField, IntField, OperationError, ValidationError, MultipleObjectsReturned, DoesNotExist
from datetime import datetime
from flask import g

from app.api import ApiError
from app.models.user import User
from app.models.category import Category


class Post(Document):
    title = StringField(required=True, max_length=100)
    content = StringField(required=True, max_length=1000)
    categories = ListField(ReferenceField(Category), default=list)
    likes = ListField(ReferenceField(User), default=list)
    likes_cnt = IntField(default=0)

    created_by = ReferenceField(User, required=True)
    created_at = DateTimeField(default=datetime.utcnow())
    updated_at = DateTimeField(default=datetime.utcnow())
    is_deleted = BooleanField(default=False)

    meta = {
        "collection": "post",
        "indexes": [{"fields": ("created_at",)}, {"fields": ("title", "categories")}, {"fields": ("is_deleted",)}],
    }

    @classmethod
    def create_post(cls, title: str, content: str, category_ids: Optional[List[ObjectId]] = None):
        # 포스트 객체 정의
        new_post = cls(title=title, content=content, created_by=g.user)
        if category_ids:
            new_post.categories = Category.objects(id__in=category_ids).all()

        # 포스트 추가 진행
        try:
            new_post.save()
        except OperationError:
            raise ApiError(message="포스트 생성 실패", status_code=500)

    @classmethod
    def get_post_list(cls, page_no: int, page_size: int, title: Optional[str] = None, category_id: Optional[ObjectId] = None):
        # 검색 쿼리 정의
        search_query = dict(is_deleted=False)
        if title:
            search_query["title__icontains"] = title
        if category_id:
            # 카테고리 id가 파라미터에 포함되어 있으면 카테고리를 조회
            try:
                category = Category.objects.get(id=category_id)
                if category:
                    search_query["categories__in"] = [category]
            except DoesNotExist:
                # 존재하지 않는 카테고리일 경우 empty list 를 return
                return list()
            except MultipleObjectsReturned:
                # 중복된 카테고리가 조회되면 error
                raise ApiError(message="카테고리 아이템(id)이 중복으로 발견되었습니다.", status_code=500)

        # 검색 결과 return
        try:
            return cls.objects(**search_query).skip((page_no - 1) * page_size).limit(page_size).exclude("content", "likes").order_by("-created_at")
        except Exception as e:
            raise ApiError(message=str(e), status_code=500)

    @classmethod
    def get_post_detail(cls, post_id: ObjectId):
        # 포스트 상세정보 조회
        try:
            return cls.objects.get(id=post_id, is_deleted=False)
        except DoesNotExist:
            raise ApiError(message="포스트를 찾을 수 없습니다.", status_code=404)
        except MultipleObjectsReturned:
            raise ApiError(message="조회 도중 에러 발생 (multiple_found_error)", status_code=500)

    def update_post(self, title: str, content: str, category_ids: Optional[List[str]] = None):
        # 수정 권한 확인
        if self.created_by != g.user:
            raise ApiError(message="해당 포스트를 수정할 권한이 없습니다.", status_code=403)

        # 업데이트 쿼리 정의
        update_query = dict(set__title=title, set__content=content, set__updated_at=datetime.utcnow())
        if category_ids:
            update_query["set__categories"] = Category.objects(id__in=category_ids).all()

        # 업데이트 진행
        try:
            self.update(**update_query)
        except OperationError:
            raise ApiError(message="포스트 수정 실패", status_code=500)

    def delete_post(self):
        # 삭제 권한 확인
        if self.created_by != g.user:
            raise ApiError(message="해당 포스트를 삭제할 권한이 없습니다.", status_code=403)

        try:
            # 포스트 삭제 진행
            self.update(set__is_deleted=True, set__updated_at=datetime.utcnow())
        except (OperationError, ValidationError):
            raise ApiError(message="포스트 삭제 실패", status_code=500)

    def add_like(self):
        # 좋아요 여부가 있으면 error
        if g.user in self.likes:
            raise ApiError(message="이미 좋아요를 누른 포스트 입니다.", status_code=409)

        # 좋아요 추가 진행
        try:
            self.update(push__likes=g.user, inc__likes_cnt=1)
        except (OperationError, ValidationError):
            raise ApiError(message="좋아요 추가 실패", status_code=500)

    def remove_like(self):
        # 좋아요 여부가 없으면 error
        if g.user not in self.likes:
            raise ApiError(message="좋아요를 누른 포스트가 아닙니다.", status_code=409)

        # 좋아요 취소 진행
        try:
            self.update(pull__likes=g.user, dec__likes_cnt=1)
        except (OperationError, ValidationError):
            raise ApiError(message="좋아요 취소 실패", status_code=500)

    @classmethod
    def remove_category_from_all(cls, category: Category):
        # 모든 포스트 document 로부터 해당 category 객체를 제거
        try:
            cls.objects(categories__in=[category]).update(pull__categories=category)
        except (OperationError, ValidationError):
            raise ApiError(message="카테고리 제거 실패", status_code=500)
