from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base
from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.resumes import router as resumes_router
from app.models import user, resume 
from app.api.jds import router as jds_router
from app.models import job_description
from app.api.matches import router as matches_router
from app.models import match_report

app = FastAPI(title="Resume Matcher API")

# Create tables (ok for MVP; later replace with Alembic migrations)
Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(resumes_router)
app.include_router(jds_router)
app.include_router(matches_router)

@app.get("/health")
def health():
    return {"status": "ok"}
