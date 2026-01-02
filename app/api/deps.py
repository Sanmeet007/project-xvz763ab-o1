from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import Token, User

security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = db.query(Token).filter(Token.token == creds.credentials).first()
    if not token:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == token.user_id).first()
    return user
