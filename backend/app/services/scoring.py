import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from numpy.typing import NDArray

# Load once
_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

DEFAULT_SKILLS = [
    "python","fastapi","django","flask","sql","postgresql","mysql",
    "docker","kubernetes","git","linux","aws","azure","gcp",
    "pandas","numpy","scikit-learn","tensorflow","pytorch","opencv",
    "rest","api","redis","celery","rabbitmq"
]
WEIGHTS = {
    "swe":{"sim": 0.55, "skills":0.45},
    "ml": {"sim": 0.45, "skills": 0.55},
    "data": {"sim": 0.40, "skills": 0.60},
}

def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()

def extract_skills(text: str, skills_list=DEFAULT_SKILLS) -> set[str]:
    t = normalize(text)
    found = set()
    for s in skills_list:
        # word boundary-ish match
        if re.search(rf"(^|[^a-z0-9]){re.escape(s)}([^a-z0-9]|$)", t):
            found.add(s)
    return found

def similarity_score(resume_text: str, jd_text: str) -> float:
    r = normalize(resume_text)
    j = normalize(jd_text)

    emb: NDArray[np.float32] = _model.encode([r, j])  # type hint added

    r_vec = emb[0].reshape(1, -1)
    j_vec = emb[1].reshape(1, -1)

    sim = cosine_similarity(r_vec, j_vec)[0][0]
    return float(sim)

def compute_match(resume_text: str, jd_text: str, preset: str = "swe") -> dict:
    weights = WEIGHTS.get(preset, WEIGHTS["swe"])

    r_skills = extract_skills(resume_text)
    j_skills = extract_skills(jd_text)

    overlap = len(r_skills & j_skills)
    total = max(len(j_skills), 1)
    skill_overlap = overlap / total  # 0..1

    sim = similarity_score(resume_text, jd_text)  # ~0..1

    score = int(round((sim * weights["sim"] + skill_overlap * weights["skills"]) * 100))
    score = max(0, min(100, score))

    missing = sorted(list(j_skills - r_skills))

    breakdown = {
    "preset": preset,
    "weights": weights,
    "similarity": round(sim * 100, 2),
    "skill_overlap": round(skill_overlap * 100, 2),
    "resume_skills": sorted(list(r_skills)),
    "jd_skills": sorted(list(j_skills)),
}


    return {"score": score, "breakdown": breakdown, "missing_skills": missing}
