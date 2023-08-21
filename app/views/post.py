from typing import Optional, List

from bson import ObjectId
from flask_apispec import use_kwargs, marshal_with, doc
from flask_classful import FlaskView, route

from app.api import ApiStatusSchema
from app.decorators.user import login_required
from app.serializers.post import PostMasterSearchFormSchema, PostCreateFormSchema, PostUpdateFormSchema, PostMasterInfoSchema, PostDetailInfoSchema
from app.models.post import Post


class PostMasterView(FlaskView):
    @route("", methods=["GET"])
    @doc(description="포스트 목록 조회", summary="포스트 목록 조회 API")
    @use_kwargs(PostMasterSearchFormSchema)
    @marshal_with(PostMasterInfoSchema(many=True), code=200, description="포스트 목록 조회 성공")
    @marshal_with(ApiStatusSchema, code=422, description="잘못된 데이터가 입력되었습니다")
    @marshal_with(ApiStatusSchema, code=500, description="포스트 목록 조회 실패")
    @login_required
    def get_list(self, page_no: int, page_size: int, title: Optional[str] = None, category_id: Optional[ObjectId] = None):
        return Post.get_post_list(page_no=page_no, page_size=page_size, title=title, category_id=category_id), 200

    @route("", methods=["POST"])
    @doc(description="포스트 추가", summary="포스트 추가 API")
    @use_kwargs(PostCreateFormSchema)
    @marshal_with(ApiStatusSchema, code=201, description="포스트 추가 성공")
    @marshal_with(ApiStatusSchema, code=422, description="잘못된 데이터가 입력되었습니다")
    @marshal_with(ApiStatusSchema, code=500, description="포스트 추가 실패")
    @login_required
    def add_post(self, title: str, content: str, category_ids: Optional[List[ObjectId]] = None):
        Post.create_post(title=title, content=content, category_ids=category_ids)
        return {"message": "생성 성공"}, 201


class PostDetailView(FlaskView):
    @route("", methods=["GET"])
    @doc(description="포스트 상세 조회", summary="포스트 상세 조회 API")
    @marshal_with(PostDetailInfoSchema, code=200, description="포스트 상세 조회 성공")
    @marshal_with(ApiStatusSchema, code=422, description="잘못된 데이터가 입력되었습니다")
    @marshal_with(ApiStatusSchema, code=404, description="조회된 포스트가 없습니다")
    @marshal_with(ApiStatusSchema, code=500, description="포스트 조회 실패")
    @login_required
    def get_post_detail(self, post_id: ObjectId):
        return Post.get_post_detail(post_id=post_id), 200

    @route("", methods=["PUT"])
    @doc(description="포스트 수정", summary="포스트 수정 API")
    @use_kwargs(PostUpdateFormSchema)
    @marshal_with(ApiStatusSchema, code=200, description="포스트 수정 성공")
    @marshal_with(ApiStatusSchema, code=403, description="수정 권한이 없습니다")
    @marshal_with(ApiStatusSchema, code=404, description="조회된 포스트가 없습니다")
    @marshal_with(ApiStatusSchema, code=500, description="포스트 수정 실패")
    @login_required
    def update_post(self, post_id: ObjectId, title: str, content: str, category_ids: Optional[List[ObjectId]] = None):
        # 포스트 검색
        post = Post.get_post_detail(post_id=post_id)

        # 포스트 수정
        post.update_post(title=title, content=content, category_ids=category_ids)
        return {"message": "포스트 수정 완료"}, 200

    @route("", methods=["DELETE"])
    @doc(description="포스트 삭제", summary="포스트 삭제 API")
    @marshal_with(ApiStatusSchema, code=204, description="포스트 삭제 성공")
    @marshal_with(ApiStatusSchema, code=403, description="삭제 권한이 없습니다")
    @marshal_with(ApiStatusSchema, code=404, description="조회된 포스트가 없습니다")
    @marshal_with(ApiStatusSchema, code=500, description="포스트 삭제 실패")
    @login_required
    def delete_post(self, post_id: ObjectId):
        # 포스트 검색
        post = Post.get_post_detail(post_id=post_id)

        # 포스트 삭제
        post.delete_post()
        return {}, 204

    @route("/like", methods=["PUT"])
    @doc(description="포스트 좋아요 추가", summary="포스트 좋아요 추가 API")
    @marshal_with(ApiStatusSchema, code=200, description="포스트 좋아요 추가 성공")
    @marshal_with(ApiStatusSchema, code=404, description="조회된 포스트가 없습니다")
    @marshal_with(ApiStatusSchema, code=409, description="이미 좋아요 추가됨")
    @marshal_with(ApiStatusSchema, code=500, description="포스트 좋아요 추가 실패")
    @login_required
    def add_like(self, post_id: ObjectId):
        # 포스트 검색
        post = Post.get_post_detail(post_id=post_id)

        # 포스트 좋아요 추가하기
        post.add_like()
        return {"message": "포스트 좋아요 추가 성공"}, 200

    @route("/like", methods=["DELETE"])
    @doc(description="포스트 좋아요 취소", summary="포스트 좋아요 취소 API")
    @marshal_with(ApiStatusSchema, code=204, description="포스트 좋아요 취소 성공")
    @marshal_with(ApiStatusSchema, code=404, description="조회된 포스트가 없습니다")
    @marshal_with(ApiStatusSchema, code=409, description="이미 좋아요 취소됨")
    @marshal_with(ApiStatusSchema, code=500, description="포스트 좋아요 취소 실패")
    @login_required
    def remove_like(self, post_id: ObjectId):
        # 포스트 검색
        post = Post.get_post_detail(post_id=post_id)

        # 포스트 좋아요 추가하기
        post.remove_like()
        return {}, 204
