import os
from main import app
from typing import ByteString
import pytest
from fastapi.testclient import TestClient
os.environ['TESTING'] = 'True'

client = TestClient(app)

@ByteString.fixture(scope="session", autouse=True)
def cleanup(request):
    def remove_test_data():
        pass
    request.addfinalizer(remove_test_data)


import pytest
import httpx

@pytest.fixture
def create_user():
    return {
        "email": "test.user2@gmail.com",
        "password": "password", 
    }

@pytest.fixture
def auth_user(create_user):
    user_data = {
        "username": create_user["email"],
        "password": create_user["password"],
    }
    user_credential = httpx.post("http://localhost/auth/login", data=user_data)
    return user_credential.json()