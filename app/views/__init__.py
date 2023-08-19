from flask import Blueprint, Flask
from flask_apispec import marshal_with

from app.api import ApiError, ApiStatusSchema
from app.utils.converter import register_path_converter
from app.views.user import UserView
from app.views.category import CategoryView
from app.views.post import PostMasterView, PostDetailView

bp: Blueprint = Blueprint("api", __name__)


def register_api(app: Flask):
    # path 변수 converter 등록
    register_path_converter(app)

    # 라우트 등록
    UserView.register(bp, route_base="/user", trailing_slash=False)
    CategoryView.register(bp, route_base="/category", trailing_slash=False)
    PostMasterView.register(bp, route_base="/post", trailing_slash=False)
    PostDetailView.register(bp, route_base="/post/<object_id:post_id>", trailing_slash=False)

    # 블루프린트를 app에 등록
    app.register_blueprint(bp)

    # 각 라우터에서 'raise ApiError(...)'를 실행할 때의 작업 등록
    app.register_error_handler(ApiError, handle_api_error)


@marshal_with(ApiStatusSchema)
def handle_api_error(err: ApiError):
    return {"message": err.message, "status_code": err.status_code}, err.status_code
