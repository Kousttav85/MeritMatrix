from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from src.database import get_all_scholarships, init_db, add_scholarship_record, delete_scholarship_record
from src.engine import calculate_match_score

app = FastAPI(title="MeritMatrix API", version="1.0.0")
init_db()

# --- Schemas ---
class StudentProfile(BaseModel):
    edu_level: str
    field: str
    cgpa: float
    family_income: int
    gender: str

class ScholarshipCreate(BaseModel):
    id: str
    title: str
    provider: str
    amount: str
    deadline: str
    min_cgpa: float
    max_income: int
    education_levels: str
    fields: str
    category: str
    gender: str
    description: str
    apply_link: str

class MatchResult(BaseModel):
    id: str
    title: str
    provider: str
    score: int
    reasons: List[str]

# --- Endpoints ---
@app.get("/")
def health_check():
    return {"status": "QuickScholar API is active."}

@app.get("/scholarships", response_model=List[Dict[str, Any]])
def read_all_scholarships():
    return get_all_scholarships()

@app.post("/match", response_model=List[MatchResult])
def match_student(profile: StudentProfile):
    scholarships = get_all_scholarships()
    results = []
    student_dict = profile.model_dump()
    for sch in scholarships:
        score, reasons = calculate_match_score(student_dict, sch)
        if score >= 50:
            results.append({
                "id": sch["id"], "title": sch["title"], "provider": sch["provider"], 
                "score": score, "reasons": reasons
            })
    return sorted(results, key=lambda x: x["score"], reverse=True)

@app.post("/admin/scholarships")
def create_scholarship(sch: ScholarshipCreate):
    data = (sch.id, sch.title, sch.provider, sch.amount, sch.deadline, sch.min_cgpa, 
            sch.max_income, sch.education_levels, sch.fields, sch.category, sch.gender, 
            sch.description, sch.apply_link)
    add_scholarship_record(data)
    return {"status": "success"}

@app.delete("/admin/scholarships/{sch_id}")
def delete_scholarship(sch_id: str):
    delete_scholarship_record(sch_id)
    return {"status": "deleted"}