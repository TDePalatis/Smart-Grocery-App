import pytest
from flask import Flask

# Import your Flask app here.
# If your app is defined in app.py, for example:
# from app import app

# MOCK setup for now if you're still building
@pytest.fixture
def client():
    app = Flask(__name__)
    
    @app.route('/')
    def home():
        return 'Hello, AI Coder!'
    
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Hello, AI Coder!' in response.data
