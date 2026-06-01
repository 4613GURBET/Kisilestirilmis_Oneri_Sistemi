"""
tests/test_routes.py
Sorumlu: Lizge
Flask route testleri
"""

import pytest
from unittest.mock import MagicMock, patch
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"]    = True
    app.config["SECRET_KEY"] = "test-secret"
    with app.test_client() as client:
        yield client


def test_index_returns_200(client):
    response = client.get("/")
    assert response.status_code == 200


def test_login_page_returns_200(client):
    response = client.get("/login")
    assert response.status_code == 200


def test_register_page_returns_200(client):
    response = client.get("/register")
    assert response.status_code == 200


def test_dashboard_redirect_if_not_logged_in(client):
    response = client.get("/dashboard")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_preferences_redirect_if_not_logged_in(client):
    response = client.get("/preferences")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]