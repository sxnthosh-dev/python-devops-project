import os

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.database import Base, get_db
from app.main import app


DB_USER = os.getenv("DB_USER", "devuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "devpassword")
DB_NAME = os.getenv("DB_NAME", "devops_db")

DB_HOST = os.getenv("TEST_DB_HOST", "localhost")
DB_PORT = os.getenv("TEST_DB_PORT", "3307")

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_mariadb_create_and_get_user():
    # Create all tables in the database before running tests
    Base.metadata.create_all(bind=engine)
    
    # Apply MariaDB dependency override only for this test.
    app.dependency_overrides[get_db] = override_get_db

    try:
        client = TestClient(app)

        create_response = client.post(
            "/users",
            json={
                "name": "MariaDB Test User",
                "email": "mariadb_test@example.com",
            },
        )

        assert create_response.status_code == 200

        created_user = create_response.json()

        assert created_user["name"] == "MariaDB Test User"
        assert created_user["email"] == "mariadb_test@example.com"
        assert "id" in created_user

        user_id = created_user["id"]

        get_response = client.get(f"/users/{user_id}")

        assert get_response.status_code == 200

        fetched_user = get_response.json()

        assert fetched_user["id"] == user_id
        assert fetched_user["name"] == "MariaDB Test User"
        assert fetched_user["email"] == "mariadb_test@example.com"

        delete_response = client.delete(f"/users/{user_id}")

        assert delete_response.status_code == 200

    finally:
        # Clean up tables after test
        Base.metadata.drop_all(bind=engine)
        # Important: don't leak the MariaDB override into other tests.
        app.dependency_overrides.clear()
