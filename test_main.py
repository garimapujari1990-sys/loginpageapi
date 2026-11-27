
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
import main1
from main1 import app

client = TestClient(app)



@pytest.fixture
def mock_db(monkeypatch):
    conn = MagicMock()
    cursor = MagicMock()

    conn.cursor.return_value = cursor

    monkeypatch.setattr("main1.db_connection", lambda: conn)

    return conn, cursor


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "api running"
    }


def test_login_success(mock_db):
    conn, cursor = mock_db

    cursor.fetchone.return_value = (1, "garima", "12345")

    response = client.post(
        "/login_check",
        json={
            "user_name": "garima",
            "password": "12345"
        }
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Login successful"


def test_invalid_username(mock_db):
    conn, cursor = mock_db

    cursor.fetchone.return_value = None

    response = client.post(
        "/login_check",
        json={
            "user_name": "wronguser",
            "password": "12345"
        }
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Invalide user name and password"


def test_invalid_password(mock_db):
    conn, cursor = mock_db

    cursor.fetchone.return_value = None

    response = client.post(
        "/login_check",
        json={
            "user_name": "garima",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Invalide user name and password"



def test_register_success(mock_db):
    conn, cursor = mock_db

    response = client.post(
        "/register_data",
        json={
            "user_name": "newuser",
            "password": "12345"
        }
    )

    assert response.status_code == 200
    assert response.json()["message"] == "sign up successful"

    cursor.execute.assert_called_once()

    conn.commit.assert_called_once()


def test_register_missing_username():
    response = client.post(
        "/register_data",
        json={
            "password": "12345"
        }
    )

    assert response.status_code == 422



def test_register_missing_password():
    response = client.post(
        "/register_data",
        json={
            "user_name": "garima"
        }
    )

    assert response.status_code == 422



def test_login_missing_password():
    response = client.post(
        "/login_check",
        json={
            "user_name": "garima"
        }
    )

    assert response.status_code == 422



def test_login_connection_closed(mock_db):
    conn, cursor = mock_db

    cursor.fetchone.return_value = (1, "garima", "12345")

    response = client.post(
        "/login_check",
        json={
            "user_name": "garima",
            "password": "12345"
        }
    )

    assert response.status_code == 200
    cursor.close.assert_called_once()
    conn.close.assert_called_once()
