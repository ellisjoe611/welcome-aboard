from bson import ObjectId
from flask_apispec import use_kwargs, marshal_with, doc
from flask_classful import FlaskView, route

from app.api import ApiStatusSchema
from app.decorators.user import login_required
from app.serializers.comment import CommentListSearchFormSchema, CommentInfoSchema, CommentCreateFormSchema
from app.models.comment import Comment
from app.models.post import Post


class CommentListView(FlaskView):
    @route("", methods=["GET"])
    @doc(description="댓글 목록 조회", summary="댓글 목록 조회 API")
    @use_kwargs(CommentListSearchFormSchema)
    @marshal_with(CommentInfoSchema(many=True), code=200, description="댓글 목록 조회 성공")
    @marshal_with(ApiStatusSchema, code=422, description="잘못된 데이터가 입력되었습니다")
    @marshal_with(ApiStatusSchema, code=500, description="댓글 목록 조회 실패")
    @login_required
    def list(self, post_id: ObjectId, page_no: int, page_size: int):
        # 포스트 조회
        post = Post.get_post_detail(post_id=post_id)

        # 댓글 목록 조회
        return Comment.get_comment_list(page_no=page_no, page_size=page_size, post=post), 200

    @route("", methods=["POST"])
    @doc(description="댓글 추가", summary="댓글 추가 API")
    @use_kwargs(CommentCreateFormSchema)
    @marshal_with(ApiStatusSchema, code=201, description="댓글 추가 성공")
    @marshal_with(ApiStatusSchema, code=422, description="잘못된 데이터가 입력되었습니다")
    @marshal_with(ApiStatusSchema, code=500, description="댓글 추가 실패")
    @login_required
    def create(self, post_id: ObjectId, content: str):
        # 포스트 조회
        post = Post.get_post_detail(post_id=post_id)

        # 댓글 추가
        Comment.create_comment(post=post, content=content)
        return {"message": "댓글 추가 성공"}, 201


class CommentInfoView(FlaskView):
    @route("", methods=["DELETE"])
    @doc(description="댓글 삭제", summary="댓글 삭제 API")
    @marshal_with(ApiStatusSchema, code=204, description="댓글 삭제 성공")
    @marshal_with(ApiStatusSchema, code=403, description="삭제 권한이 없습니다")
    @marshal_with(ApiStatusSchema, code=404, description="댓글 조회 실패")
    @marshal_with(ApiStatusSchema, code=500, description="댓글 삭제 실패")
    @login_required
    def delete(self, comment_id: ObjectId):
        # 댓글 조회
        comment = Comment.get_comment_by_id(comment_id=comment_id)

        # 댓글 삭제 진행
        comment.delete_comment()
        return {}, 204

    @route("/like", methods=["PUT"])
    @doc(description="댓글 좋아요 추가", summary="댓글 좋아요 추가 API")
    @marshal_with(ApiStatusSchema, code=200, description="댓글 좋아요 추가 성공")
    @marshal_with(ApiStatusSchema, code=404, description="댓글 조회 실패")
    @marshal_with(ApiStatusSchema, code=409, description="이미 좋아요 추가됨")
    @marshal_with(ApiStatusSchema, code=500, description="댓글 좋아요 추가 실패")
    @login_required
    def like(self, comment_id: ObjectId):
        # 댓글 조회
        comment = Comment.get_comment_by_id(comment_id=comment_id)

        # 댓글 좋아요 추가 진행
        comment.add_like()
        return {"message": "댓글 좋아요 추가 성공"}, 200

    @route("/like", methods=["DELETE"])
    @doc(description="댓글 좋아요 취소", summary="댓글 좋아요 취소 API")
    @marshal_with(ApiStatusSchema, code=200, description="댓글 좋아요 취소 성공")
    @marshal_with(ApiStatusSchema, code=404, description="댓글 조회 실패")
    @marshal_with(ApiStatusSchema, code=409, description="이미 좋아요 취소됨")
    @marshal_with(ApiStatusSchema, code=500, description="댓글 좋아요 취소 실패")
    @login_required
    def unlike(self, comment_id: ObjectId):
        # 댓글 조회
        comment = Comment.get_comment_by_id(comment_id=comment_id)

        # 댓글 좋아요 추가 진행
        comment.remove_like()
        return {"message": "댓글 좋아요 취소 성공"}, 200
