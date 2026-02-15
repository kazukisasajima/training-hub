from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from app.core.exceptions import AppError
from app.schemas.error import ErrorResponse


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
        payload = ErrorResponse(code=exc.code, message=exc.message, detail=exc.detail).model_dump()
        # codeに応じてHTTPを切りたい場合は、ここでマッピングしてもよい
        status = 400
        if exc.code == "NOT_FOUND":
            status = 404
        elif exc.code == "CONFLICT":
            status = 409
        elif exc.code == "UNAUTHORIZED":
            status = 401
        elif exc.code == "FORBIDDEN":
            status = 403
        return JSONResponse(status_code=status, content=payload)

    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(_: Request, exc: IntegrityError) -> JSONResponse:
        # DBの一意制約などは基本409に統一
        payload = ErrorResponse(
            code="CONFLICT",
            message="Resource conflict.",
            detail=str(exc.orig) if exc.orig else str(exc),
        ).model_dump()
        return JSONResponse(status_code=409, content=payload)

    @app.exception_handler(Exception)
    async def unhandled_error_handler(_: Request, exc: Exception) -> JSONResponse:
        payload = ErrorResponse(
            code="INTERNAL_ERROR",
            message="Unexpected error occurred.",
            detail=str(exc),
        ).model_dump()
        return JSONResponse(status_code=500, content=payload)
