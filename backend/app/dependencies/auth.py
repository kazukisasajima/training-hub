from fastapi import HTTPException, Request
from app.core.security import decode_token

# ここはあなたのユーザー取得方法に合わせて実装してください
# ※ ここは最終的に「既存の users テーブル/CRUD」に置き換える箇所です。
# 例: crud.get_user_by_email(...)
def get_user_by_email(email: str):
    # TODO: DBから取得する実装に差し替え
    if email == "test@example.com":
        return {"id": 1, "email": email, "hashed_password": "$2b$12$KIX..." }  # ダミー
    return None

def get_current_user(request: Request):
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

    user = get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user