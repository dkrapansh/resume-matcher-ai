# AI Resume Matcher

An AI-powered web application that evaluates how well a resume matches a job description using semantic embeddings and skill-based scoring.

Built with FastAPI, PostgreSQL, React (Vite), and Sentence-Transformers.

---

##  Overview

Recruiters manually evaluate resumes against job descriptions, which is time-consuming and subjective.

This project automates that process by:

- Extracting text from resumes (PDF/DOCX)
- Identifying relevant technical skills
- Computing semantic similarity using transformer embeddings
- Generating a weighted match score
- Producing a downloadable PDF report

---

##  Architecture

**Backend:** FastAPI  
**Frontend:** React (Vite + Tailwind)  
**Database:** PostgreSQL  
**AI Model:** Sentence-Transformers (MiniLM via HuggingFace Transformers)  
**PDF Reports:** ReportLab  

Flow:

1. User uploads resume
2. Resume text is extracted and stored
3. User adds job description
4. Matching engine:
   - Skill extraction (regex-based)
   - Embedding similarity (MiniLM)
   - Weighted scoring (preset-based)
5. Match report saved in database
6. PDF report generated on demand

---

##  Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- JWT Authentication
- Sentence-Transformers
- ReportLab

### Frontend
- React (Vite)
- TailwindCSS
- React Router
- Axios

---

##  Matching Logic

The overall score is computed using a weighted combination:

- Semantic similarity (embedding-based)
- Skill overlap score (keyword-based extraction)

Different presets allow role-specific weighting:
- SWE
- ML
- Data

Example:

```text
Final Score = (Similarity × W₁) + (Skill Overlap × W₂)
```
 
Where:

- **Similarity** is computed using sentence-transformer embeddings  
  (cosine similarity between resume and job description vectors)

- **Skill Overlap** =  
  (Number of overlapping extracted skills ÷ Total JD skills)

Weights depend on selected preset:

| Preset | Similarity Weight | Skill Weight |
|--------|-------------------|-------------|
| SWE    | 0.60              | 0.40        |
| ML     | 0.45              | 0.55        |
| Data   | 0.50              | 0.50        |

This allows the scoring engine to adapt depending on the target role.

---

### Example Breakdown

If:

- Similarity = 0.47  
- Skill Overlap = 0.75  
- Preset = ML  

Then:

```text
Score = (0.47 × 0.45) + (0.75 × 0.55)
```

 
Final Score ≈ **62 / 100**

The response also includes:

- Extracted resume skills
- Extracted JD skills
- Missing skills
- Raw similarity percentage
- Skill overlap percentage

---

## Authentication

- JWT-based authentication
- Password hashing using bcrypt
- Protected routes for all user-specific resources
- Token-based access control for reports and uploads

---

## API Endpoints

### Auth
- `POST /auth/register`
- `POST /auth/login`

### Resumes
- `POST /resumes/upload`
- `GET /resumes`

### Job Descriptions
- `POST /jds`
- `GET /jds`

### Matching
- `POST /matches`
- `GET /matches`
- `GET /matches/{id}`
- `GET /matches/{id}/pdf`

---

## Running Locally

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend runs at:  
http://127.0.0.1:8000

---

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at:  
http://localhost:5173

---

##  Future Improvements

- Async background job queue for resume processing
- Embedding caching (Redis)
- Improved NLP-based skill extraction
- CI/CD pipeline
- Production deployment (Render + Vercel)
- Role-based analytics dashboard

---

## Why This Project Matters

This project demonstrates:

- Real-world backend architecture
- AI model integration inside production-style APIs
- JWT-based authentication design
- Database modeling with relational integrity
- File handling and streaming (PDF reports)
- Full-stack integration (React + FastAPI)

---
