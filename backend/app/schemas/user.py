from datetime import datetime
from uuid import UUID
import re

from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    """
    パスワード仕様（一般的な実装）:

    - 入力（プレーンパスワード）はDBに保存しない。保存するのはハッシュ文字列（hashed_password）。
    - hashed_password は bcrypt 等で生成された文字列で、保存用に VARCHAR(255) 等を確保するのが一般的。

    入力できるパスワード要件:
    - 長さ: 8〜12文字
    - 使用可能: 半角英字・半角数字・半角記号（& を含む）
    - 使用不可: 空白、改行、日本語、全角
    """

    password: str = Field(
        min_length=8,
        max_length=12,
        examples=["P@ssw0rd&12"],
        description="8-12 chars. Half-width letters/numbers/symbols only (no spaces).",
    )

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        # 半角英数字・半角記号のみ（空白や全角、日本語は弾く）
        # 許可範囲: '!'(0x21) ～ '~'(0x7E)
        if not re.fullmatch(r"[!-~]+", v):
            raise ValueError("password must use half-width letters/numbers/symbols only (no spaces, no full-width).")

        # bcryptの72bytes制限は、8〜12文字運用なら通常問題にならないが、
        # 念のため「サーバが500で落ちる」ことを防ぐために残す
        if len(v.encode("utf-8")) > 72:
            raise ValueError("password is too long for bcrypt (72 bytes limit).")

        return v


class UserRead(UserBase):
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(default=None, min_length=8)
