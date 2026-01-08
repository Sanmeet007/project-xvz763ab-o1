from datetime import datetime
from pathlib import Path
import os
import uuid
from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Form,
)
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.db.models import User
from app.schemas.user import UserProfileUpdate, UserProfileResponse, SummaryLoadRequest, SummaryResponse

router = APIRouter(prefix="/api/user", tags=["User"])


@router.get("/profile", response_model=UserProfileResponse)
def get_profile(user=Depends(get_current_user)):
    """
    Get current logged-in user's profile.
    """
    return user


@router.post("/profile", response_model=UserProfileResponse)
def update_profile(
    payload: UserProfileUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Update textual profile fields.
    """
    db_user: User = db.query(User).filter(User.id == user.id).first()  # type: ignore
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if payload.full_name is not None:
        db_user.full_name = payload.full_name
    if payload.bio is not None:
        db_user.bio = payload.bio
    if payload.specialization is not None:
        db_user.specialization = payload.specialization
    if payload.phone is not None:
        db_user.phone = payload.phone

    db.commit()
    db.refresh(db_user)

    return db_user


@router.post("/profile/image", response_model=UserProfileResponse)
async def upload_profile_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Accept image input for profile photo.
    Saves file locally under 'media/profile' and stores URL in DB.
    """
    if file.content_type not in {"image/jpeg", "image/png", "image/webp"}:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    media_root = Path("media/profile")
    media_root.mkdir(parents=True, exist_ok=True)

    ext = os.path.splitext(file.filename)[1] or ".jpg"
    filename = f"{uuid.uuid4().hex}{ext}"
    file_path = media_root / filename

    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    image_url = f"/media/profile/{filename}"

    db_user: User = db.query(User).filter(User.id == user.id).first()  # type: ignore
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.image_url = image_url
    db.commit()
    db.refresh(db_user)

    return db_user


@router.post("/summary", response_model=SummaryResponse)
def load_summary(
    payload: SummaryLoadRequest,
    user=Depends(get_current_user),
):
    """
    Summary loading stub. 
    Connect this to your med_search_service or prescription_extraction_service.
    """
    # TODO: replace with real lookup
    return SummaryResponse(
        consultation_id=payload.consultation_id,
        summary_text=f"Summary for {payload.consultation_id} (stub)",
        created_at=datetime.utcnow(),
    )
