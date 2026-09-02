from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.database import Base, get_db
from app.main import app

# Use an in-memory SQLite database for fast, isolated testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


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
    # First create a user to fetch
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