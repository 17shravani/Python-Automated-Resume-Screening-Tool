try:
    from sentence_transformers import SentenceTransformer, util
    import torch
    HAS_ST = True
except ImportError:
    HAS_ST = False

class TalentScorer:
    """
    Advanced Scoring Engine using Neural Embeddings (MiniLM).
    """
    def __init__(self):
        # Using a small, fast, yet powerful model
        if HAS_ST:
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
        else:
            self.model = None
        self.soft_skills_db = ["leadership", "communication", "teamwork", "agile", "problem solving", "mentoring", "collaboration", "adaptability"]

    def compute_similarity(self, resume_text, jd_text):
        """
        Calculates Semantic Cosine Similarity.
        """
        if not HAS_ST:
            return 85.50  # Mock score if torch isn't installed
            
        resume_emb = self.model.encode(resume_text, convert_to_tensor=True)
        jd_emb = self.model.encode(jd_text, convert_to_tensor=True)
        
        cosine_sim = util.cos_sim(resume_emb, jd_emb)
        return round(float(cosine_sim[0][0]) * 100, 2)

    def infer_soft_skills(self, resume_text):
        text_lower = resume_text.lower()
        found = []
        for skill in self.soft_skills_db:
            if skill in text_lower:
                found.append(skill.capitalize())
        score = (len(found) / 5) * 100 if len(found) <= 5 else 100
        return min(score, 100), found

    def generate_interview_questions(self, missing_skills, matched_skills):
        questions = []
        if missing_skills:
            ms = missing_skills[0]
            if matched_skills:
                qs = matched_skills[0]
                questions.append(f"We noticed you don't have direct experience with {ms}, but you do know {qs}. How would you leverage your knowledge of {qs} to quickly learn {ms}?")
            else:
                questions.append(f"How would you approach learning {ms} on the job?")
        
        if len(missing_skills) > 1:
            questions.append(f"Our role requires {missing_skills[1]}. Can you describe a time you had to learn a new technology rapidly?")
            
        if not questions:
            questions.append("You seem to have all the required technical skills! What is the most challenging technical problem you've solved recently?")
            
        return questions

    def calculate_final_score(self, resume_data, jd_data):
        """
        Calculates a weighted score based on:
        - Semantic Similarity (60%)
        - Skill Coverage (30%)
        - Experience Match (10%)
        """
        # 1. Semantic Similarity
        sim_score = self.compute_similarity(resume_data['text'], jd_data['text'])
        
        # 2. Skill Coverage
        resume_skills = set([s.lower() for s in resume_data['extracted']['skills']])
        jd_skills = set([s.lower() for s in jd_data['required_skills']])
        
        if not jd_skills:
            skill_score = 100
            missing_skills = []
            matched_skills = list(resume_skills)
        else:
            matches = resume_skills.intersection(jd_skills)
            skill_score = (len(matches) / len(jd_skills)) * 100
            missing_skills = list(jd_skills - resume_skills)
            matched_skills = list(matches)
            
        # Format for output
        missing_skills = [s.capitalize() for s in missing_skills]
        matched_skills = [s.capitalize() for s in matched_skills]
            
        # 3. Experience Match
        req_exp = jd_data.get('min_experience', 0)
        has_exp = resume_data['extracted']['experience']
        
        if has_exp >= req_exp:
            exp_score = 100
        else:
            exp_score = (has_exp / req_exp) * 100 if req_exp > 0 else 100

        # 4. Soft Skills Inference
        soft_score, found_soft_skills = self.infer_soft_skills(resume_data['text'])

        # Weighted Final Score
        final_score = (0.6 * sim_score) + (0.3 * skill_score) + (0.1 * exp_score)
        
        questions = self.generate_interview_questions(missing_skills, matched_skills)
        
        return {
            "overall_score": round(final_score, 2),
            "breakdown": {
                "semantic_similarity": sim_score,
                "skill_score": round(skill_score, 2),
                "experience_score": round(exp_score, 2),
                "soft_skills_score": round(soft_score, 2)
            },
            "missing_skills": missing_skills,
            "matched_skills": matched_skills,
            "found_soft_skills": found_soft_skills,
            "interview_questions": questions
        }

if __name__ == "__main__":
    scorer = TalentScorer()
    print("Scorer initialized.")
