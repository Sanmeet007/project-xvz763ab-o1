from pydantic import BaseModel, EmailStr
from datetime import date

class SignupRequest(BaseModel):
    email: EmailStr
    username: str
    dob: date
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
