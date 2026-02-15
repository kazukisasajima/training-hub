from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class AppError(Exception):
    code: str
    message: str
    detail: Optional[Any] = None


@dataclass
class NotFoundError(AppError):
    pass


@dataclass
class ConflictError(AppError):
    pass


@dataclass
class UnauthorizedError(AppError):
    pass


@dataclass
class ForbiddenError(AppError):
    pass
