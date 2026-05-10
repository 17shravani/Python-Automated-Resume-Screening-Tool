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
    
    print("--- NexusTalent Quantum AI Sanity Check ---")
    
    # 1. Test Parser
    parser = ResumeParser()
    # Check for john_doe_perfect.txt or similar
    sample_resume_path = "data/resumes/john_doe_perfect.txt"
    if not os.path.exists(sample_resume_path):
        # Create data/resumes if not exists
        os.makedirs("data/resumes", exist_ok=True)
        with open(sample_resume_path, "w") as f:
            f.write("John Doe. Python Developer with 6 years experience. Skills: Python, SQL, AWS, Leadership.")
            
    text = parser.parse(sample_resume_path)
    print(f"[OK] Parser: Extracted {len(text)} characters")

    # 2. Test Extractor
    extractor = EntityExtractor()
    extracted = extractor.parse_all(text)
    print(f"[OK] Extractor: Found skills: {extracted['skills']}")

    # 3. Test Scorer
    scorer = TalentScorer()
    
    # Ensure JD exists
    jd_path = "data/jd/python_dev_jd.txt"
    if not os.path.exists(jd_path):
        os.makedirs("data/jd", exist_ok=True)
        with open(jd_path, "w") as f:
            f.write("Senior Python Developer role. Requirements: Python, SQL, AWS. 5 years experience.")
            
    jd_text = Path(jd_path).read_text()
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
    print(f"[OK] Scorer: Final Score: {result['overall_score']}%")
    print(f"[OK] Intelligence Panel: {list(result['agent_verdicts'].keys())}")
    print(f"[OK] Trajectory: {result['trajectory']}")
    print(f"[OK] Market Value: {result['market_value']}")
    
    print("\nNEXUSTALENT QUANTUM AI IS FULLY OPERATIONAL!")

except Exception as e:
    print(f"\n[!] An error occurred: {e}")
    import traceback
    traceback.print_exc()


