import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    DB_USER = os.getenv("DB_USER", "devuser")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "devpassword")
    DB_NAME = os.getenv("DB_NAME", "devops_db")
    DB_HOST = os.getenv("DB_HOST", "db")
    DB_PORT = os.getenv("DB_PORT", "3306")

    database_url: str = os.getenv(
        "DATABASE_URL",
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


settings = Settings()