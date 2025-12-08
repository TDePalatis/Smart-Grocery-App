# SmartGroceryApp/tests/conftest.py
import pytest

from SmartGroceryApp import create_app
from SmartGroceryApp.extensions import db

# Try to import an existing TestingConfig; if not present, define one.
try:
    from SmartGroceryApp.config import TestingConfig as _BaseTestingConfig  # type: ignore
except Exception:
    _BaseTestingConfig = object  # fallback if module or class doesn't exist


class PytestConfig(_BaseTestingConfig):
    """Test config for pytest runs."""
    TESTING = True
    # In-memory DB for speed/isolation
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Ensure CSRF doesn't block form posts during tests (if using Flask-WTF)
    WTF_CSRF_ENABLED = False

    # Make sure external services don't initialize
    OPENAI_API_KEY = None


@pytest.fixture(scope="session")
def app():
    app = create_app(config_class=PytestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    c = app.test_client()
    if hasattr(c, "cookie_jar"):
        c.cookie_jar.clear()  # ensure no leftover auth
    return c
