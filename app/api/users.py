from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import crud
from app.db.database import get_db
from app.schemas.user import UserCreate, UserResponse


router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserResponse)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    existing_user = crud.user.get_user_by_email(
        db,
        email=user.email,
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )

    try:
        return crud.user.create_user(
            db=db,
            user=user,
        )
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )


@router.get("", response_model=list[UserResponse])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.user.get_users(
        db,
        skip=skip,
        limit=limit,
    )


@router.get("/{user_id}", response_model=UserResponse)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    db_user = crud.user.get_user(
        db,
        user_id=user_id,
    )

    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return db_user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    user = crud.user.get_user(
        db,
        user_id=user_id,
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    existing_user = crud.user.get_user_by_email(
        db,
        email=user_data.email,
    )

    if existing_user and existing_user.id != user_id:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )

    try:
        return crud.user.update_user(
            db=db,
            user_id=user_id,
            user_data=user_data,
        )
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.user.get_user(db, user_id)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    crud.user.delete_user(db, user_id)

    return {"message": "User deleted successfully"}