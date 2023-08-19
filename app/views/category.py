from typing import Optional

from flask_apispec import doc, use_kwargs, marshal_with
from flask_classful import FlaskView, route

from app.api import ApiStatusSchema
from app.decorators.user import login_required, master_login_required
from app.serializers.category import CategorySearchFormSchema, CategoryInfoSchema, CategoryCreateFormSchema, CategoryDeleteFormSchema
from app.models.category import Category
from app.models.post import Post


class CategoryView(FlaskView):
    @route("/list", methods=["GET"])
    @doc(description="카테고리 목록 확인", summary="카테고리 목록 확인 API")
    @use_kwargs(CategorySearchFormSchema)
    @marshal_with(CategoryInfoSchema(many=True), code=200, description="조회 성공")
    @marshal_with(ApiStatusSchema, code=500, description="조회 실패")
    @login_required
    def list(self, name: Optional[str] = None):
        return Category.get_category_list(name=name), 200

    @route("/add", methods=["POST"])
    @doc(description="카테고리 추가 (관리자용)", summary="카테고리 추가 API")
    @use_kwargs(CategoryCreateFormSchema)
    @marshal_with(ApiStatusSchema, code=201, description="생성 성공")
    @marshal_with(ApiStatusSchema, code=409, description="중복 확인됨")
    @marshal_with(ApiStatusSchema, code=500, description="생성 실패")
    @master_login_required
    def add(self, name: str):
        Category.create_category(name=name)
        return {"message": "생성 성공"}, 201

    @route("/delete", methods=["DELETE"])
    @doc(description="카테고리 삭제 (관리자용)", summary="카테고리 삭제 API")
    @use_kwargs(CategoryDeleteFormSchema)
    @marshal_with(ApiStatusSchema, code=204, description="삭제 성공")
    @marshal_with(ApiStatusSchema, code=404, description="조회 실패")
    @marshal_with(ApiStatusSchema, code=422, description="요청 양식 미흡")
    @marshal_with(ApiStatusSchema, code=500, description="삭제 실패")
    @master_login_required
    def delete(self, name: str):
        # 카테고리 조회
        category = Category.get_category_by_name(name=name)

        # 포스트들 중 해당 카테고리가 있으면 제거하기
        Post.remove_category_from_all(category=category)

        # 최종적으로 삭제
        category.delete_category()
        return {"message": "삭제 성공"}, 204
