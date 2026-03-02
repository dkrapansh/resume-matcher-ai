from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.resume import Resume
from app.models.user import User
from app.services.resume_parser import extract_text

router = APIRouter(prefix="/resumes", tags=["resumes"])

@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    filename = file.filename or ""
    content = await file.read()

    try:
        text = extract_text(filename, content)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not text:
        raise HTTPException(status_code=400, detail="Could not extract text from file")

    resume = Resume(
        user_id=current_user.id,
        filename=filename,
        raw_text=text[:200000]  # safety cap
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)

    return {
        "id": str(resume.id),
        "filename": resume.filename,
        "chars_extracted": len(resume.raw_text)
    }

@router.get("")
def list_resumes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rows = db.query(Resume).filter(Resume.user_id == current_user.id).order_by(Resume.created_at.desc()).all()
    return [
        {"id": str(r.id), "filename": r.filename, "created_at": r.created_at}
        for r in rows
    ]
