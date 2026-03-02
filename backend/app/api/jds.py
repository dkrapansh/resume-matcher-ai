from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.job_description import JobDescription
from app.models.user import User
from app.schemas.job_description import JDCreate

router = APIRouter(prefix="/jds", tags=["job_descriptions"])

@router.post("")
def create_jd(payload: JDCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    jd = JobDescription(
        user_id=current_user.id,
        title=payload.title,
        company=payload.company,
        raw_text=payload.raw_text[:200000],
    )
    db.add(jd)
    db.commit()
    db.refresh(jd)
    return {"id": str(jd.id), "title": jd.title, "company": jd.company}

@router.get("")
def list_jds(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    rows = db.query(JobDescription).filter(JobDescription.user_id == current_user.id).order_by(JobDescription.created_at.desc()).all()
    return [{"id": str(r.id), "title": r.title, "company": r.company, "created_at": r.created_at} for r in rows]
