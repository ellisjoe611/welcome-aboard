from typing import Optional

from flask_apispec import doc, use_kwargs, marshal_with
from flask_classful import FlaskView, route

from app.api import ApiStatusSchema
from app.decorators.user import login_required, master_login_required
from app.models.tag import Tag
from app.serializers.tag import TagSearchFormSchema, TagInfoSchema, TagCreateFormSchema


class TagView(FlaskView):
    @route("/list", methods=["GET"])
    @doc(description="태그 목록 확인", summary="태그 목록 확인 API")
    @use_kwargs(TagSearchFormSchema)
    @marshal_with(TagInfoSchema(many=True), code=200, description="조회 성공")
    @marshal_with(ApiStatusSchema, code=500, description="조회 실패")
    @login_required
    def list(self, page_no: int, page_size: int, name: Optional[str] = None):
        return Tag.list_tag(page_no=page_no, page_size=page_size, name=name), 200

    @route("/add", methods=["POST"])
    @doc(description="태그 추가 (관리자용)", summary="태그 추가 API")
    @use_kwargs(TagCreateFormSchema)
    @marshal_with(ApiStatusSchema, code=201, description="생성 성공")
    @marshal_with(ApiStatusSchema, code=409, description="중복 확인됨")
    @marshal_with(ApiStatusSchema, code=500, description="생성 실패")
    @master_login_required
    def add(self, name: str):
        Tag.create_tag(name=name)
        return {"message": "생성 성공"}, 201
