from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.models.resume import Resume
from app.models.job_description import JobDescription
from app.models.match_report import MatchReport
from app.schemas.match import MatchCreate
from app.services.scoring import compute_match

from fastapi.responses import Response
from app.services.report_pdf import build_report_pdf

router = APIRouter(prefix="/matches", tags=["matches"])

@router.post("")
def create_match(payload: MatchCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    resume = db.query(Resume).filter(Resume.id == payload.resume_id, Resume.user_id == current_user.id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    jd = db.query(JobDescription).filter(JobDescription.id == payload.jd_id, JobDescription.user_id == current_user.id).first()
    if not jd:
        raise HTTPException(status_code=404, detail="Job description not found")

    result = compute_match(resume.raw_text, jd.raw_text, preset=payload.preset)

    report = MatchReport(
        user_id=current_user.id,
        resume_id=resume.id,
        jd_id=jd.id,
        score=result["score"],
        score_breakdown=result["breakdown"],
        missing_skills=result["missing_skills"],
    )
    db.add(report)
    db.commit()
    db.refresh(report)

    return {"id": str(report.id), "score": report.score, "missing_skills": report.missing_skills, "breakdown": report.score_breakdown}

@router.get("")
def list_matches(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    rows = db.query(MatchReport).filter(MatchReport.user_id == current_user.id).order_by(MatchReport.created_at.desc()).all()
    return [{"id": str(r.id), "score": r.score, "created_at": r.created_at, "resume_id": str(r.resume_id), "jd_id": str(r.jd_id)} for r in rows]

@router.get("/{match_id}")
def get_match(match_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    r = db.query(MatchReport).filter(
        MatchReport.id == match_id,
        MatchReport.user_id == current_user.id
    ).first()

    if not r:
        raise HTTPException(status_code=404, detail="Match report not found")

    return {
        "id": str(r.id),
        "score": r.score,
        "missing_skills": r.missing_skills,
        "breakdown": r.score_breakdown,
        "created_at": r.created_at,
        "resume_id": str(r.resume_id),
        "jd_id": str(r.jd_id),
    }

@router.get("/{match_id}/pdf")
def get_match_pdf(match_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    r = db.query(MatchReport).filter(
        MatchReport.id == match_id,
        MatchReport.user_id == current_user.id
    ).first()
    if not r:
        raise HTTPException(status_code=404, detail="Match report not found")

    report_dict = {
        "id": str(r.id),
        "score": r.score,
        "missing_skills": r.missing_skills,
        "breakdown": r.score_breakdown,
        "created_at": r.created_at.isoformat(),
        "resume_id": str(r.resume_id),
        "jd_id": str(r.jd_id),
    }

    pdf_bytes = build_report_pdf(report_dict)

    filename = f"match_report_{match_id}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )
