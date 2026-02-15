from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.dependencies.db import get_db
from app.schemas.user import UserCreate, UserRead, UserUpdate
# from app.crud.user import get_by_id, get_user_by_email, create_user, update_user, delete_user
from app.crud import user as user_crud # こっちの方がどこから呼び出した関数か分かりやすい
from app.core.exceptions import NotFoundError

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)) -> UserRead:
    existing = user_crud.get_user_by_email(db, email=user_in.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    user = user_crud.create_user(db, user_in)
    return user

# @router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
# def create_user(payload: UserCreate, db: Session = Depends(get_db)) -> UserRead:
#     return user_crud.create_user(db, payload)


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)) -> UserRead:
    user = user_crud.get_by_id(db, user_id=user_id)
    if not user:
        raise NotFoundError(code="NOT_FOUND", message="User not found.")
    return user


@router.patch("/{user_id}", response_model=UserRead)
def update_user(user_id: int, user_in: UserUpdate, db: Session = Depends(get_db)) -> UserRead:
    user = user_crud.update_user(db, user_id, user_in)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)) -> None:
    user_crud.delete_user(db, user_id)
    return None