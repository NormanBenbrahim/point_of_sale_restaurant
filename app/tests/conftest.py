import pytest

from app.api import create_app


@pytest.fixture(scope='session')
def app():
    """
    setup tests for api
    """

    params = {
        'DEBUG': False,
        'TESTING': True
    }

    _app = create_app(settings_override=params)

    # give the app context
    context = _app.app_context()
    context.push()

    yield _app

    context.pop()


@pytest.fixture(scope='function')
def client(app):
    """
    setup app client, gets executed each test function bc of yield
    """
    yield app.test_client()
