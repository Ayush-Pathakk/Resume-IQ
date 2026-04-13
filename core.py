from dataclasses import dataclass, field
from typing import List
import re
import pdfplumber
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from config import SKILLS


@dataclass
class ResumeResult:
    filename: str
    score: float
    matched_skills: List[str] = field(default_factory=list)
    error: str = ""


def extract_text(pdf_path: str) -> str:
    try:
        with pdfplumber.open(pdf_path) as pdf:
            return " ".join(page.extract_text() or "" for page in pdf.pages)
    except Exception as e:
        raise RuntimeError(f"PDF read failed: {e}")


def clean(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def extract_skills(text: str) -> List[str]:
    return [s for s in SKILLS if s in text]


def score(resume_text: str, jd_text: str) -> float:
    vec = TfidfVectorizer()
    try:
        matrix = vec.fit_transform([resume_text, jd_text])
        return round(float(cosine_similarity(matrix[0], matrix[1])[0][0]) * 100, 2)
    except Exception:
        return 0.0


def process_resume(pdf_path: str, jd_clean: str, filename: str) -> ResumeResult:
    try:
        raw = extract_text(pdf_path)
        cleaned = clean(raw)
        s = score(cleaned, jd_clean)
        skills = extract_skills(cleaned)
        return ResumeResult(filename=filename, score=s, matched_skills=skills)
    except RuntimeError as e:
        return ResumeResult(filename=filename, score=0.0, error=str(e))
