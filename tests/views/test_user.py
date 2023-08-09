import pytest


class Test_user:
    @pytest.fixture()
    def temp_user(self):
        return dict(email="test@aimmo.co.kr", name="nobody", password="qwerty123!")

    @pytest.fixture(scope="function")
    def subject(self, client, temp_user):
        pass
