from fastapi import Header, HTTPException, Request

def require_csrf(request: Request, x_csrf_token: str | None = Header(default=None)):
    cookie_token = request.cookies.get("csrf_token")
    if not cookie_token or not x_csrf_token or cookie_token != x_csrf_token:
        raise HTTPException(status_code=403, detail="CSRF token missing or invalid")