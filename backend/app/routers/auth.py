from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.crud import user as user_crud
from app.core.security import verify_password, create_access_token
from app.core.exceptions import UnauthorizedError
from app.schemas.token import TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> TokenResponse:
    user = user_crud.get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise UnauthorizedError(code="UNAUTHORIZED", message="Invalid credentials.")
    access_token = create_access_token(subject=str(user.user_id))
    return TokenResponse(access_token=access_token)
