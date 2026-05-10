from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
import uvicorn
import uuid
import json
import sqlite3
from typing import List, Optional
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.parser import ResumeParser
from src.extractor import EntityExtractor
from src.scorer import TalentScorer

app = FastAPI(title="NexusTalent Quantum AI API")
db_path = "db/talent.db"

# Initialize DB
def init_db():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS jobs 
                 (id TEXT PRIMARY KEY, title TEXT, description TEXT, skills TEXT, min_experience INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS rankings 
                 (job_id TEXT, candidate_name TEXT, score REAL, details TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Initialize Engines
parser = ResumeParser()
extractor = EntityExtractor()
scorer = TalentScorer()

class Job(BaseModel):
    title: str
    description: str
    skills: List[str]
    min_experience: int

@app.post("/jobs/create")
async def create_job(job: Job):
    job_id = str(uuid.uuid4())
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO jobs VALUES (?, ?, ?, ?, ?)", 
              (job_id, job.title, job.description, ",".join(job.skills), job.min_experience))
    conn.commit()
    conn.close()
    return {"job_id": job_id, "message": "Job created successfully"}

@app.post("/screen/{job_id}")
async def screen_resume(job_id: str, candidate_name: str = Form(...), file: UploadFile = File(...)):
    # 1. Fetch Job Data
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM jobs WHERE id=?", (job_id,))
    job_row = c.fetchone()
    conn.close()
    
    if not job_row:
        raise HTTPException(status_code=404, detail="Job not found")
        
    jd_data = {
        "title": job_row[1],
        "text": job_row[2],
        "required_skills": job_row[3].split(","),
        "min_experience": job_row[4]
    }

    # 2. Process Resume
    temp_path = f"data/resumes/{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())
    
    resume_text = parser.parse(temp_path)
    extracted_data = extractor.parse_all(resume_text)
    
    resume_data = {
        "text": resume_text,
        "extracted": extracted_data
    }

    # 3. Score
    scoring_result = scorer.calculate_final_score(resume_data, jd_data)

    # 4. Save Ranking
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO rankings VALUES (?, ?, ?, ?)", 
              (job_id, candidate_name, scoring_result['overall_score'], json.dumps(scoring_result)))
    conn.commit()
    conn.close()

    return {
        "candidate": candidate_name,
        "score": scoring_result['overall_score'],
        "breakdown": scoring_result['breakdown'],
        "extracted_skills": extracted_data['skills'],
        "missing_skills": scoring_result.get('missing_skills', []),
        "matched_skills": scoring_result.get('matched_skills', []),
        "found_soft_skills": scoring_result.get('found_soft_skills', []),
        "interview_questions": scoring_result.get('interview_questions', []),
        "agent_verdicts": scoring_result.get('agent_verdicts', {}),
        "trajectory": scoring_result.get('trajectory', []),
        "market_value": scoring_result.get('market_value', "N/A")
    }



@app.get("/rankings/{job_id}")
async def get_rankings(job_id: str):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT candidate_name, score, details FROM rankings WHERE job_id=? ORDER BY score DESC", (job_id,))
    rows = c.fetchall()
    conn.close()
    
    results = []
    for row in rows:
        results.append({
            "name": row[0],
            "score": row[1],
            "details": json.loads(row[2])
        })
    return results

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
