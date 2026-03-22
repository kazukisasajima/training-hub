from pydantic import BaseModel, EmailStr
from uuid import UUID


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class MeResponse(BaseModel):
    user_id: UUID
    name: str