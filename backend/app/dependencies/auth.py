from fastapi import HTTPException, Request, Depends
from sqlalchemy.orm import Session

from app.core.security import decode_token
from app.crud.user import get_user_by_email
from app.dependencies.db import get_db


def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = decode_token(token)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token")

    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = get_user_by_email(db, email)

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user