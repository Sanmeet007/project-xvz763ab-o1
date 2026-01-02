from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.auth import SignupRequest, LoginRequest
from app.db.models import User, Token
from app.api.deps import get_db, get_current_user
from app.core.security import hash_password, verify_password, generate_token

router = APIRouter(prefix="/api", tags=["Auth"])

@router.post("/signup")
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="User already exists")

    user = User(
        email=payload.email,
        username=payload.username,
        dob=payload.dob,
        password=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token_value = generate_token()
    db.add(Token(token=token_value, user_id=user.id))
    db.commit()

    return {"error": False, "access_token": token_value}

@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password): # type: ignore
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token_value = generate_token()
    db.add(Token(token=token_value, user_id=user.id))
    db.commit()

    return {"error": False, "access_token": token_value}

@router.get("/me")
def me(user=Depends(get_current_user)):
    return {
        "email": user.email,
        "username": user.username,
        "dob": user.dob,
    }
