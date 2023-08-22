import pytest
from flask import Flask
from flask.testing import FlaskClient


@pytest.fixture()
def app() -> Flask:
    from wsgi import app

    yield app


@pytest.fixture()
def client(app: Flask) -> FlaskClient:
    return app.test_client(use_cookies=False)
