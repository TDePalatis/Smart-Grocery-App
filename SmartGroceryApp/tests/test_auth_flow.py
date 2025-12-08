# tests/test_auth_flow.py
from flask import url_for
from SmartGroceryApp.extensions import db
from SmartGroceryApp.models import User
from werkzeug.security import check_password_hash

def register(client, email="test@example.com", password="StrongPass!123"):
    return client.post("/auth/register", data={"email": email, "password": password}, follow_redirects=True)

def login(client, email="test@example.com", password="StrongPass!123"):
    return client.post("/auth/login", data={"email": email, "password": password}, follow_redirects=True)

def test_register_creates_user(client):
    resp = register(client)
    assert resp.status_code == 200  # after redirect
    # user exists in DB
    user = User.query.filter_by(email="test@example.com").first()
    assert user is not None
    assert check_password_hash(user.password_hash, "StrongPass!123")

def test_register_duplicate_email_shows_error(client):
    register(client)
    resp = register(client)
    assert resp.status_code == 200
    assert b"Email already exists" in resp.data  # message from your template

def test_login_success_redirects_to_reports(client):
    register(client)
    resp = login(client)
    assert resp.status_code == 200
    # reports page renders; it might include “Reports” or a known element
    assert b"Reports" in resp.data or b"reports" in resp.data

def test_login_failure_shows_error(client):
    register(client)
    resp = login(client, password="WrongPass")
    assert resp.status_code == 200
    assert b"Incorrect email or password" in resp.data


def test_reports_requires_login(client):
    # ensure we're not authenticated
    client.get("/auth/logout", follow_redirects=True)

    resp = client.get("/reports/", follow_redirects=True)
    assert resp.status_code == 200
    assert b"<form" in resp.data and b"password" in resp.data
