# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
import pytest

from api.index import app


@pytest.fixture()
def client():
    app.testing = True
    with app.test_client() as test_client:
        yield test_client
