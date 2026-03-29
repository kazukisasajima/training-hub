from pydantic import BaseModel, EmailStr, Field
from uuid import UUID


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class MeResponse(BaseModel):
    user_id: UUID
    name: str
    email: EmailStr


class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class UpdateMeRequest(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=8)