import os
import secrets
from fastapi import APIRouter, Depends, Response, HTTPException

from app.schemas.auth import LoginRequest, MeResponse
from app.core.security import create_access_token, verify_password
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

COOKIE_SECURE = os.getenv("COOKIE_SECURE", "false").lower() == "true"

# TODO: DB実装に差し替え
def get_user_by_email(email: str):
    # 仮ユーザー（最初の動作確認用）
    # パスワードは "password" を bcrypt でハッシュしたものを入れてください
    # 生成例: pythonで hash_password("password") を一回実行して貼る
    # docker compose exec backend python -c "from app.core.security import hash_password; print(hash_password('password'))"
    # 上記を実行して生成されたハッシュをhashed_passwordに貼る
    if email == "test@example.com":
        return {
            "id": 1,
            "email": email,
            "hashed_password": "$2b$12$zoZB/3dglKiqPrCrrymdw.HeYzggRPMgRiujZTs2IANfqXTV6kUgm",
        }
    return None

@router.post("/login")
def login(body: LoginRequest, response: Response):
    user = get_user_by_email(body.email)

    # ユーザー列挙対策：存在しない/不一致は同じメッセージ
    if (not user) or (not verify_password(body.password, user["hashed_password"])):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(subject=user["email"])

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
    return {"id": user["id"], "email": user["email"]}

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token", path="/")
    response.delete_cookie("csrf_token", path="/")
    return {"ok": True}