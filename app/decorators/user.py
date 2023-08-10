import jwt
from jwt.exceptions import DecodeError, InvalidTokenError
from functools import wraps
from flask import request, current_app, g

from app.api import ApiError


def login_required(func):
    @wraps(func)
    def _wrapper(*args, **kwargs):
        do_setup_flask_g()

        # 지정된 함수 실행하기
        return func(*args, **kwargs)

    return _wrapper


def master_login_required(func):
    @wraps(func)
    def _wrapper(*args, **kwargs):
        do_setup_flask_g()

        if g.is_master is not True:
            raise ApiError(message="Not authorized user", status_code=403)
        return func(*args, **kwargs)

    return _wrapper


def do_setup_flask_g():
    if "X-Auth-Token" not in request.headers:
        raise ApiError(message="User login required", status_code=401)
    try:
        payload = jwt.decode(request.headers.get("X-Auth-Token"), key=current_app.config["TOKEN_KEY"], algorithms=[current_app.config["ALGORITHM"]])
    except (DecodeError, InvalidTokenError):
        raise ApiError(message="Not valid authorization token", status_code=401)

    g.email, g.is_master = payload["email"], payload["is_master"]
