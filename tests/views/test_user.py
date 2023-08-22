from typing import Any, Dict

import jwt
import pytest
from flask import current_app
from flask.testing import FlaskClient


@pytest.fixture()
def user_login_form() -> Dict:
    return dict(email="tester03@aimmo.co.kr", password="qwer1234")


@pytest.fixture()
def token_response(client: FlaskClient, user_login_form: Dict) -> Any:
    response = client.post("/user/login", data=user_login_form)
    return response


@pytest.fixture()
def token_response_json(token_response) -> Dict:
    return token_response.json


class TestUser:
    class TestLogin:
        def test_check_login_status(self, token_response):
            assert token_response.status_code == 200

        def test_check_token(self, token_response_json):
            assert isinstance(token_response_json, dict) and "token" in token_response_json

    @pytest.fixture()
    def token(self, token_response_json: Dict) -> str:
        return token_response_json["token"]

    class TestUserInfo:
        @pytest.fixture()
        def user_info(self, client: FlaskClient, token: str):
            response = client.get("/user/info", headers={"X-Auth-Token": token})
            return response

        def test_check_user_info(self, user_info):
            assert user_info.json is not None
            assert user_info.json["is_master"] is False
