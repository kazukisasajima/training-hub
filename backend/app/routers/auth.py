from sqlalchemy.orm import Session
import os
import secrets
from fastapi import APIRouter, Depends, Response, HTTPException

from app.schemas.auth import LoginRequest, MeResponse, SignupRequest, UpdateMeRequest
from app.schemas.user import UserCreate
from app.core.security import create_access_token, verify_password, hash_password
from app.crud.user import get_user_by_email, create_user
from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from app.dependencies.csrf import require_csrf

router = APIRouter(prefix="/auth", tags=["auth"])

COOKIE_SECURE = os.getenv("COOKIE_SECURE", "false").lower() == "true"


@router.post("/login")
def login(body: LoginRequest, response: Response, db: Session = Depends(get_db)):
    user = get_user_by_email(db, email=body.email)

    # ユーザー列挙対策：存在しない/不一致は同じメッセージ
    if (not user) or (not verify_password(body.password, user.password)):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(subject=user.email)

    # CSRF token（JSから読めるCookie）
    csrf_token = secrets.token_urlsafe(32)

    # httpOnly JWT Cookie
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite="lax",
        path="/",
        max_age=60 * 60,  # 例: 1h
    )

    # CSRF Cookie（httpOnlyなし）
    response.set_cookie(
        key="csrf_token",
        value=csrf_token,
        httponly=False,
        secure=COOKIE_SECURE,
        samesite="lax",
        path="/",
        max_age=60 * 60,
    )

    return {"ok": True}


@router.get("/me", response_model=MeResponse)
def me(user=Depends(get_current_user)):
    return {"user_id": user.user_id, "name": user.name, "email": user.email}


@router.patch("/me", response_model=MeResponse)
def update_me(
    body: UpdateMeRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
    _=Depends(require_csrf),
):
    if body.email and body.email != user.email:
        existing = get_user_by_email(db, email=body.email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        user.email = body.email

    if body.name is not None:
        user.name = body.name

    if body.password:
        user.password = hash_password(body.password)

    db.commit()
    db.refresh(user)

    return {"user_id": user.user_id, "name": user.name, "email": user.email}


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token", path="/")
    response.delete_cookie("csrf_token", path="/")
    return {"ok": True}


@router.post("/signup")
def signup(body: SignupRequest, response: Response, db: Session = Depends(get_db)):
    # 既存ユーザー確認
    existing = get_user_by_email(db, email=body.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_in = UserCreate(name=body.name, email=body.email, password=body.password)
    # ユーザー作成
    user = create_user(db, user_in)

    # そのままログインさせる（おすすめ）
    token = create_access_token(subject=user.email)

    csrf_token = secrets.token_urlsafe(32)

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite="lax",
        path="/",
    )

    response.set_cookie(
        key="csrf_token",
        value=csrf_token,
        httponly=False,
        secure=COOKIE_SECURE,
        samesite="lax",
        path="/",
    )

    return {"ok": True}