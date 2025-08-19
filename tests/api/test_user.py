import os
import signal
import subprocess
import time
from dataclasses import dataclass

import pytest
import requests


@dataclass
class User:
    id: int
    name: str
    email: str


@pytest.fixture(scope="class", autouse=True)
def run_server():
    proc = subprocess.Popen(["python", "-m", "logitech.api.mock_api"])
    time.sleep(1)  # wait for Flask to boot
    yield
    os.kill(proc.pid, signal.SIGTERM)


class TestMockAPI:

    BASE_URL = "http://127.0.0.1:5003"

    def test_retrieve_list_of_users(self):
        try:
            response = requests.get(f"{self.BASE_URL}/users")
            assert response.status_code == 200

            users = response.json()
            assert isinstance(users, list)

            for user_data in users:
                user = User(**user_data)
                assert isinstance(user, User)

        except requests.exceptions.RequestException as e:
            assert False, f"Request failed: {e}"
        except TypeError as e:
            assert False, f"User data validation failed: {e}"

    @pytest.mark.parametrize(
        "user_data",
        [
            ({"name": "Jan Kowalski", "email": "jan.kowalski@example.com"}),
            ({}),
            ({"email": "jan.kowalski@example.com"}),
            ({"name": "Jan Kowalski"}),
        ],
    )
    def test_create_new_user(self, user_data: int):
        try:
            response = requests.post(f"{self.BASE_URL}/users", json=user_data)

            if response.status_code == 400:
                assert response.json() == {"error": "Invalid data"}
            elif response.status_code == 201:
                created_user_data = response.json()
                created_user = User(**created_user_data)

                assert user_data["email"] == created_user.email
                assert user_data["name"] == created_user.name

            assert response.status_code in (201, 400)

        except requests.exceptions.RequestException as e:
            assert False, f"Request failed: {e}"

    @pytest.mark.parametrize(
        "user_id, user_data",
        [
            (999, {}),  # HTTP 500
            (
                1,
                {"id": 1, "name": "Alice", "email": "alice@example.com"},
            ),  # User from sample data - HTTP 200
            (
                2,
                {"id": 2, "name": "Bob", "email": "bob@example.com"},
            ),  # User from sample data - HTTP 200
            (9999, {}),  # HTTP 404
        ],
    )
    def test_retrieve_user_data(self, user_id: int, user_data: dict):
        try:
            response = requests.get(f"{self.BASE_URL}/users/{user_id}")

            if response.status_code == 500:
                assert response.json() == {"error": "Internal Server Error"}
            elif response.status_code == 404:
                assert response.json() == {"error": "User not found"}
            elif response.status_code == 200:
                retrieved_user_data = response.json()
                retrieved_user = User(**retrieved_user_data)

                assert user_data["email"] == retrieved_user.email
                assert user_data["name"] == retrieved_user.name

            assert response.status_code in (200, 404, 500)

        except requests.exceptions.RequestException as e:
            assert False, f"Request failed: {e}"
