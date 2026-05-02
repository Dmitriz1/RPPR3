import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# =========================
# 🔐 AUTH TESTS
# =========================

def test_register_success():
    response = client.post("/auth/register", params={
        "username": "testuser",
        "password": "1234"
    })
    assert response.status_code == 200
    assert "user_id" in response.json()


def test_register_duplicate():
    client.post("/auth/register", params={
        "username": "dupuser",
        "password": "1234"
    })

    response = client.post("/auth/register", params={
        "username": "dupuser",
        "password": "1234"
    })

    assert response.status_code == 400


def test_login_success():
    client.post("/auth/register", params={
        "username": "loginuser",
        "password": "1234"
    })

    response = client.post("/auth/login", params={
        "username": "loginuser",
        "password": "1234"
    })

    assert response.status_code == 200
    assert "token" in response.json()


def test_login_invalid():
    response = client.post("/auth/login", params={
        "username": "wrong",
        "password": "wrong"
    })

    assert response.status_code == 401


# =========================
# 👨‍🎓 STUDENTS TESTS
# =========================

def get_token():
    client.post("/auth/register", params={
        "username": "user1",
        "password": "1234"
    })
    res = client.post("/auth/login", params={
        "username": "user1",
        "password": "1234"
    })
    return res.json()["token"]


def test_get_students_unauthorized():
    response = client.get("/students/")
    assert response.status_code == 422 or response.status_code == 401


def test_get_students_authorized():
    token = get_token()

    response = client.get(
        "/students/",
        headers={"authorization": token}
    )

    assert response.status_code == 200


def test_create_student_success():
    token = get_token()

    response = client.post(
        "/students/",
        headers={"authorization": token},
        json={
            "name": "Ivan",
            "faculty": "CS",
            "subject": "Math",
            "grade": 90
        }
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Ivan"


def test_create_student_unauthorized():
    response = client.post(
        "/students/",
        json={
            "name": "Ivan",
            "faculty": "CS",
            "subject": "Math",
            "grade": 90
        }
    )

    assert response.status_code == 422 or response.status_code == 401


# =========================
# 🎓 FILTER TESTS
# =========================

def test_students_by_faculty_success():
    token = get_token()

    client.post(
        "/students/",
        headers={"authorization": token},
        json={
            "name": "Anna",
            "faculty": "Physics",
            "subject": "Optics",
            "grade": 80
        }
    )

    response = client.get(
        "/students/faculty/Physics",
        headers={"authorization": token}
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_students_by_faculty_unauthorized():
    response = client.get("/students/faculty/Physics")
    assert response.status_code == 422 or response.status_code == 401


# =========================
# ⚡ TASKS TESTS
# =========================

def test_import_task_success():
    token = get_token()

    response = client.post(
        "/tasks/import",
        headers={"authorization": token},
        params={"file_path": "test.csv"}
    )

    assert response.status_code == 200
    assert response.json()["message"] == "import started"


def test_import_task_unauthorized():
    response = client.post(
        "/tasks/import",
        params={"file_path": "test.csv"}
    )

    assert response.status_code == 422 or response.status_code == 401