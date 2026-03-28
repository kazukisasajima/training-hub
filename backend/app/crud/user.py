from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password
from app.core.exceptions import NotFoundError, ConflictError


def get_by_id(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user_in: UserCreate) -> User:
    hashed_password = hash_password(user_in.password)
    existing = get_user_by_email(db, email=user_in.email)
    if existing:
        raise ConflictError(code="CONFLICT", message="Email already registered.")

    user = User(
        name=user_in.name,
        email=user_in.email,
        password=hashed_password,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user_id: int, user_in: UserUpdate) -> User:
    user = get_by_id(db, user_id)
    if not user:
        raise NotFoundError(code="NOT_FOUND", message="User not found.")

    if user_in.email and user_in.email != user.email:
        existing = get_user_by_email(db, user_in.email)
        if existing:
            raise ConflictError(code="CONFLICT", message="Email already exists.")
        user.email = user_in.email

    if user_in.password:
        user.password = hash_password(user_in.password)


    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> None:
    user = get_by_id(db, user_id)
    if not user:
        raise NotFoundError(code="NOT_FOUND", message="User not found.")

    db.delete(user)
    db.commit()
