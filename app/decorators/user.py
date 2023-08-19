import jwt
from jwt.exceptions import DecodeError, InvalidTokenError
from functools import wraps
from flask import request, current_app, g

from app.api import ApiError
from app.models.user import User


def login_required(func):
    @wraps(func)
    def _wrapper(*args, **kwargs):
        do_setup_flask_g()

        try:
            return func(*args, **kwargs)
        except ApiError as e:
            raise e
        except Exception as e:
            raise ApiError(message=str(e), status_code=500)

    return _wrapper


def master_login_required(func):
    @wraps(func)
    def _wrapper(*args, **kwargs):
        do_setup_flask_g()

        if g.user.is_master is not True:
            raise ApiError(message="Not authorized user", status_code=403)

        try:
            return func(*args, **kwargs)
        except ApiError as e:
            raise e
        except Exception as e:
            raise ApiError(message=str(e), status_code=500)

    return _wrapper


def do_setup_flask_g():
    if "X-Auth-Token" not in request.headers:
        raise ApiError(message="User login required", status_code=401)
    try:
        payload = jwt.decode(request.headers.get("X-Auth-Token"), key=current_app.config["TOKEN_KEY"], algorithms=[current_app.config["ALGORITHM"]])
        g.user = User.objects(email=payload["email"], is_deleted=False).first()
        if not g.user:
            raise ApiError(message="User not found based on submitted token", status_code=401)
        print(f"[decorators/user.py] id: {g.user.id} / email: {g.user.email} / is_master: {g.user.is_master} / is_deleted: {g.user.is_deleted}")
    except (DecodeError, InvalidTokenError):
        raise ApiError(message="Not valid authorization token", status_code=401)
