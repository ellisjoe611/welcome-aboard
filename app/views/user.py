import bcrypt
from flask import g
from flask_classful import FlaskView, route
from flask_apispec import use_kwargs, marshal_with, doc
from typing import Optional
from marshmallow import ValidationError
from mongoengine import OperationError

from app.api import ApiError, ApiStatusSchema
from app.serializers.user import UserCreateFormSchema, UserLoginFormSchema, UserInfoSchema, UserSearchFormSchema, UserUpdateFormSchema
from app.serializers.auth_token import AuthTokenSchema
from app.models.user import User
from app.models.auth_token import AuthToken
from app.decorators.user import login_required, master_login_required


class UserView(FlaskView):
    @route("/signup", methods=["POST"])
    @doc(description="회원 가입", summary="신규 회원 가입 API")
    @use_kwargs(UserCreateFormSchema)
    @marshal_with(ApiStatusSchema, code=201, description="가입 성공")
    @marshal_with(ApiStatusSchema, code=422, description="잘못된 데이터가 입력되었습니다")
    @marshal_with(ApiStatusSchema, code=500, description="DB 업데이트 실패")
    def signup(self, email: str, name: str, password: str, subscribing: Optional[bool] = False):
        # 이메일 중복 여부 확인
        if User.objects(email=email).count() > 0:
            raise ApiError(message="이미 존재하거나 등록되었던 사용자입니다", status_code=409)

        # 사용자 생성해서 업데이트
        try:
            new_user = User(email=email, name=name, password=bcrypt.hashpw(password=password.encode("utf-8"), salt=bcrypt.gensalt()))
            if subscribing is True:
                new_user.subscribing = True
            new_user.save()
        except ValidationError:
            raise ApiError(message="잘못된 데이터가 입력되었습니다", status_code=422)
        except OperationError:
            raise ApiError(message="DB 업데이트 실패", status_code=500)
        else:
            return {"message": "가입 성공"}, 201

    @route("/login", methods=["POST"])
    @doc(description="로그인", summary="로그인 API")
    @use_kwargs(UserLoginFormSchema)
    @marshal_with(AuthTokenSchema, code=200, description="로그인 성공")
    @marshal_with(ApiStatusSchema, code=401, description="로그인 실패")
    @marshal_with(ApiStatusSchema, code=500, description="처리 도중 오류")
    def login(self, email: str, password: str):
        # 사용자 정보 조회
        user = User.get_user_info(email=email)

        # 비밀번호 해독 & 확인
        if user.check_pw(password=password) is not True:
            raise ApiError(message="비밀번호가 일치하지 않습니다", status_code=401)

        # 사용자의 토큰을 생성 후 return
        return AuthToken.get_new_token(email=user.email, is_master=user.is_master), 200

    @route("/info", methods=["GET"])
    @doc(description="회원 정보 확인", summary="회원 정보 확인 api")
    @marshal_with(UserInfoSchema, code=200, description="조회 성공")
    @marshal_with(ApiStatusSchema, code=404, description="조회된 정보 없음")
    @marshal_with(ApiStatusSchema, code=500, description="조회 실패")
    @login_required
    def info(self):
        return User.get_user_info(email=g.user.email), 200

    @route("/update", methods=["PUT"])
    @doc(description="회원 정보 수정", summary="회원 정보 수정 api")
    @use_kwargs(UserUpdateFormSchema)
    @marshal_with(AuthTokenSchema, code=200, description="회원 정보 수정 완료")
    @marshal_with(ApiStatusSchema, code=404, description="회원 확인 실패")
    @marshal_with(ApiStatusSchema, code=422, description="요청 body 확인 필요")
    @marshal_with(ApiStatusSchema, code=500, description="처리 도중 오류")
    @login_required
    def update(self, subscribing: bool, change_pw: bool, password: Optional[str] = None, new_password: Optional[str] = None):
        if subscribing is None and not change_pw:
            raise ApiError(message="수정할 데이터가 없습니다.", status_code=422)

        # 회원 정보 조회
        user = User.get_user_info(email=g.user.email)

        # 회원 정보 수정
        user.update_user_info(change_pw=change_pw, password=password, new_password=new_password, subscribing=subscribing)
        return {"message": "회원 정보 수정 완료"}, 200

    @route("/list", methods=["GET"])
    @doc(description="회원 목록 확인", summary="회원 리스트 확인 (임시용)")
    @use_kwargs(UserSearchFormSchema)
    @marshal_with(UserInfoSchema(many=True), code=200, description="사용자 리스트 조회 (임시)")
    @master_login_required
    def list(self, page_no: int, page_size: int, email: Optional[str] = None):
        return User.get_user_list(page_no=page_no, page_size=page_size, email=email), 200
