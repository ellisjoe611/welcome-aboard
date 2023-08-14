from flask_apispec import use_kwargs, marshal_with, doc
from flask_classful import FlaskView, route

from app.api import ApiStatusSchema
from app.decorators.user import login_required
from app.serializers.post import PostSearchFormSchema


@login_required
class PostView(FlaskView):
    @route("/signup", methods=["GET"])
    @doc(description="포스트 조회", summary="포스트 조회 API")
    @use_kwargs(PostSearchFormSchema)
    @marshal_with(PostInfoSchema, code=201, description="가입 성공")
    @marshal_with(ApiStatusSchema, code=422, description="잘못된 데이터가 입력되었습니다")
    @marshal_with(ApiStatusSchema, code=500, description="DB 업데이트 실패")
    def posts(self):
        pass