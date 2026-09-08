import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.database import Base, get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_and_teardown_db():
    """Create fresh tables for each test and clear them afterward."""
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    
    yield
    
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


def test_create_user():
    response = client.post(
        "/users", json={"name": "Alice Doe", "email": "alice@example.com"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Alice Doe"
    assert data["email"] == "alice@example.com"
    assert "id" in data


def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_user_by_id():
    create_res = client.post(
        "/users", json={"name": "Bob Smith", "email": "bob@example.com"}
    )
    user_id = create_res.json()["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Bob Smith"


def test_update_user():
    create_res = client.post(
        "/users", json={"name": "Charlie", "email": "charlie@example.com"}
    )
    user_id = create_res.json()["id"]

    response = client.put(
        f"/users/{user_id}",
        json={"name": "Charlie Updated", "email": "charlie@example.com"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Charlie Updated"


def test_delete_user():
    create_res = client.post(
        "/users", json={"name": "David", "email": "david@example.com"}
    )
    user_id = create_res.json()["id"]

    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "User deleted successfully"}

    # Verify user is gone
    get_res = client.get(f"/users/{user_id}")
    assert get_res.status_code == 404
def test_create_duplicate_email():
    payload = {
        "name": "Alice",
        "email": "alice@example.com",
    }

    first_response = client.post("/users", json=payload)
    assert first_response.status_code == 200

    response = client.post("/users", json=payload)
    assert response.status_code == 409
    assert response.json()["detail"] == "Email already registered"


def test_get_nonexistent_user():
    response = client.get("/users/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_update_nonexistent_user():
    response = client.put(
        "/users/9999",
        json={
            "name": "Nobody",
            "email": "nobody@example.com",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_delete_nonexistent_user():
    response = client.delete("/users/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_invalid_email():
    response = client.post(
        "/users",
        json={
            "name": "Invalid User",
            "email": "not-an-email",
        },
    )

    assert response.status_code == 422


def test_name_too_short():
    response = client.post(
        "/users",
        json={
            "name": "A",
            "email": "valid@example.com",
        },
    )

    assert response.status_code == 422

def test_update_with_duplicate_email():
    first_response = client.post(
        "/users",
        json={
            "name": "Alice",
            "email": "alice@example.com",
        },
    )
    assert first_response.status_code == 200

    second_response = client.post(
        "/users",
        json={
            "name": "Bob",
            "email": "bob@example.com",
        },
    )
    assert second_response.status_code == 200

    bob_id = second_response.json()["id"]

    response = client.put(
        f"/users/{bob_id}",
        json={
            "name": "Bob Updated",
            "email": "alice@example.com",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"