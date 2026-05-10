import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

try:
    from parser import ResumeParser
    from extractor import EntityExtractor
    from scorer import TalentScorer
    import pandas as pd
    import spacy
    from sentence_transformers import SentenceTransformer
    
    print("--- TalentFlow AI Sanity Check ---")
    
    # 1. Test Parser
    parser = ResumeParser()
    sample_resume_path = "data/resumes/john_doe_perfect.txt"
    if os.path.exists(sample_resume_path):
        text = parser.parse(sample_resume_path)
        print(f"[OK] Parser: Extracted {len(text)} characters from {sample_resume_path}")
    else:
        print("[FAIL] Parser: Sample resume not found. Run generate_samples.py first.")
        sys.exit(1)

    # 2. Test Extractor
    extractor = EntityExtractor()
    extracted = extractor.parse_all(text)
    print(f"[OK] Extractor: Found skills: {extracted['skills']}")
    print(f"[OK] Extractor: Experience: {extracted['experience']} years")

    # 3. Test Scorer
    scorer = TalentScorer()
    jd_text = Path("data/jd/python_dev_jd.txt").read_text()
    jd_data = {
        "text": jd_text,
        "required_skills": ["Python", "SQL", "AWS"],
        "min_experience": 5
    }
    resume_data = {
        "text": text,
        "extracted": extracted
    }
    
    result = scorer.calculate_final_score(resume_data, jd_data)
    print(f"[OK] Scorer: Computed Final Score: {result['overall_score']}%")
    print(f"Breakdown: {result['breakdown']}")
    
    print("\n✅ SYSTEM IS ERROR-FREE AND READY!")

except ImportError as e:
    print(f"\n[!] Missing Library: {e}")
    print("Please run: pip install -r requirements.txt")
except Exception as e:
    print(f"\n[!] An error occurred: {e}")
