from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import UnauthorizedError
from app.crud import user as user_crud
from app.dependencies.db import get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise UnauthorizedError(code="UNAUTHORIZED", message="Invalid token.")
    except JWTError:
        raise UnauthorizedError(code="UNAUTHORIZED", message="Invalid token.")

    user = user_crud.get_by_id(db, user_id=user_id)
    if user is None:
        raise UnauthorizedError(code="UNAUTHORIZED", message="User not found.")
    return user
