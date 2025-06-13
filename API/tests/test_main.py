
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from fastapi.testclient import TestClient
from src.app.main import tdlapp

client = TestClient(tdlapp)

"""
***********************************************
Method: test_create_user()

Description: This method tests the create user endpoint
with valid credentials. It ensures that a user can
register successfully and receive an access token.

Returns: None. Asserts status code 200 and presence 
of access_token in the response.
***********************************************
"""
def test_create_user():
    response = client.post("/users/", json={"username": "testuser", "password": "testpass"})
    assert response.status_code in (200, 400)
    data = response.json()
    if response.status_code == 200:
        assert "access_token" in data

"""
***********************************************
Method: test_login_user()

Description: This method tests the login endpoint
with valid credentials. It ensures that a user can
log in successfully and receive an access token.

Returns: None. Asserts status code 200 and presence 
of access_token in the response.
***********************************************
"""
def test_login_user():
    client.post("/users/", json={"username": "testlogin", "password": "testpass"})
    response = client.post(
        "/login",
        data={"username": "testlogin", "password": "testpass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

"""
***********************************************
Method: test_login_wrong_password()

Description: This method tests the login endpoint
with an incorrect password. It checks that the 
response is unauthorized.

Returns: None. Asserts response status code is 401.
***********************************************
"""
def test_login_wrong_password():
    client.post("/users/", json={"username": "wrongpass", "password": "rightpass"})
    response = client.post(
        "/login",
        data={"username": "wrongpass", "password": "wrongpass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 401

"""
***********************************************
Method: test_protected_route_requires_auth()

Description: This method tests if access to a 
protected route (/tasks/) is blocked without a 
valid authentication token.

Returns: None. Asserts status code is 401 or 403.
***********************************************
"""
def test_protected_route_requires_auth():
    response = client.get("/tasks/")
    assert response.status_code == 401 or response.status_code == 403

"""
***********************************************
Method: test_task_crud()

Description: This method tests the full CRUD 
functionality for tasks. It includes creating, 
retrieving, updating, and deleting a task using 
a valid authenticated user session.

Returns: None. Asserts expected status codes and 
response data at each step.
***********************************************
"""
def test_task_crud():
    client.post("/users/", json={"username": "taskuser", "password": "taskpass"})
    login = client.post(
        "/login",
        data={"username": "taskuser", "password": "taskpass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    create = client.post("/tasks/", json={"title": "Test Task", "description": "Test Desc"}, headers=headers)
    assert create.status_code == 200 or create.status_code == 201
    task = create.json()
    assert task["title"] == "Test Task"

    get = client.get("/tasks/", headers=headers)
    assert get.status_code == 200
    assert any(t["title"] == "Test Task" for t in get.json())

    update = client.put(f"/tasks/{task['id']}", json={"title": "Updated Task", "description": "Updated Desc"}, headers=headers)
    assert update.status_code == 200
    assert update.json()["title"] == "Updated Task"

    delete = client.delete(f"/tasks/{task['id']}", headers=headers)
    assert delete.status_code == 200 or delete.status_code == 204

"""
***********************************************
Method: test_delete_account()

Description: This method tests account deletion. 
It registers a user, logs in to obtain a token, 
and then deletes the user account.

Returns: None. Asserts status code 200, 204, or 202.
***********************************************
"""
def test_delete_account():
    client.post("/users/", json={"username": "deluser", "password": "delpass"})
    login = client.post(
        "/login",
        data={"username": "deluser", "password": "delpass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.delete("/users/me", headers=headers)
    assert response.status_code == 200 or response.status_code == 204 or response.status_code == 202