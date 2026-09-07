from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
import logging

from app.db.models import User
from app.schemas.user import UserCreate

logger = logging.getLogger(__name__)


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    logger.info("Database: Creating user with email=%s", user.email)
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)

    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        logger.warning("Database integrity error while creating user with email=%s", user.email)
        raise


def update_user(db: Session, user_id: int, user_data: UserCreate):
    logger.info("Database: Updating user id=%s", user_id)
    db_user = get_user(db, user_id)

    if not db_user:
        return None

    db_user.name = user_data.name
    db_user.email = user_data.email

    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        logger.warning("Database integrity error while updating user id=%s", user_id)
        raise


def delete_user(db: Session, user_id: int):
    logger.info("Database: Deleting user id=%s", user_id)
    db_user = get_user(db, user_id)

    if not db_user:
        return None

    db.delete(db_user)
    db.commit()

    return db_user