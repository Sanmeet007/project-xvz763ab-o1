from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    bio: Optional[str] = None
    specialization: Optional[str] = None
    phone: Optional[str] = None


class UserProfileResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    dob: datetime
    full_name: Optional[str] = None
    bio: Optional[str] = None
    specialization: Optional[str] = None
    phone: Optional[str] = None
    image_url: Optional[str] = None

    class Config:
        from_attributes = True


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ForgotPasswordConfirm(BaseModel):
    token: str
    new_password: str


class SummaryLoadRequest(BaseModel):
    consultation_id: str


class SummaryResponse(BaseModel):
    consultation_id: str
    summary_text: str
    created_at: datetime
