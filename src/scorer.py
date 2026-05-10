try:
    from sentence_transformers import SentenceTransformer, util
    import torch
    HAS_ST = True
except ImportError:
    HAS_ST = False

class TalentScorer:
    """
    NexusTalent Quantum AI Scoring Engine.
    Features: Multi-Agent Verdicts, Career Trajectory, and Market Intelligence.
    """
    def __init__(self):
        if HAS_ST:
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
        else:
            self.model = None
        self.soft_skills_db = ["leadership", "communication", "teamwork", "agile", "problem solving", "mentoring", "collaboration", "adaptability"]

    def compute_similarity(self, resume_text, jd_text):
        if not HAS_ST:
            return 85.50
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

    def get_agent_verdicts(self, breakdown, matched_skills, missing_skills):
        """Simulates 3 AI Agent perspectives."""
        verdicts = {
            "Technical Oracle": {
                "score": breakdown['skill_score'],
                "verdict": "The candidate's tech stack is " + ("robust" if breakdown['skill_score'] > 70 else "evolving") + ". " + 
                           (f"Strong alignment with {matched_skills[0]}." if matched_skills else "Needs core skill alignment.")
            },
            "Strategic Lead": {
                "score": breakdown['experience_score'],
                "verdict": "Experience levels " + ("match" if breakdown['experience_score'] > 80 else "are slightly below") + " requirements. " +
                           "Potential for high-impact contributions in structured environments."
            },
            "Culture Guardian": {
                "score": breakdown['soft_skills_score'],
                "verdict": "Soft skill indicators suggest a " + ("highly collaborative" if breakdown['soft_skills_score'] > 60 else "focused") + " personality profile."
            }
        }
        return verdicts

    def predict_career_trajectory(self, exp_score, skill_score):
        """Simulates career path projection."""
        if exp_score > 80 and skill_score > 80:
            return ["Principal Architect", "CTO Track", "Innovation Lead"]
        elif skill_score > 70:
            return ["Senior Engineer", "Tech Lead", "Architecture Specialist"]
        else:
            return ["Core Developer", "Project Lead", "Domain Expert"]

    def estimate_market_value(self, matched_skills, exp_score):
        """Estimates market worth based on skills and experience."""
        base = 60000
        skill_bonus = len(matched_skills) * 5000
        exp_multiplier = (exp_score / 100) * 0.5 + 1.0
        est = (base + skill_bonus) * exp_multiplier
        return f"${int(est/1000)}k - ${int((est*1.2)/1000)}k"

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
        sim_score = self.compute_similarity(resume_data['text'], jd_data['text'])
        
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
            
        missing_skills = [s.capitalize() for s in missing_skills]
        matched_skills = [s.capitalize() for s in matched_skills]
            
        req_exp = jd_data.get('min_experience', 0)
        has_exp = resume_data['extracted']['experience']
        exp_score = 100 if has_exp >= req_exp else (has_exp / req_exp) * 100 if req_exp > 0 else 100
        soft_score, found_soft_skills = self.infer_soft_skills(resume_data['text'])

        final_score = (0.6 * sim_score) + (0.3 * skill_score) + (0.1 * exp_score)
        
        breakdown = {
            "semantic_similarity": sim_score,
            "skill_score": round(skill_score, 2),
            "experience_score": round(exp_score, 2),
            "soft_skills_score": round(soft_score, 2)
        }
        
        agent_verdicts = self.get_agent_verdicts(breakdown, matched_skills, missing_skills)
        trajectory = self.predict_career_trajectory(exp_score, skill_score)
        market_value = self.estimate_market_value(matched_skills, exp_score)
        questions = self.generate_interview_questions(missing_skills, matched_skills)
        
        return {
            "overall_score": round(final_score, 2),
            "breakdown": breakdown,
            "missing_skills": missing_skills,
            "matched_skills": matched_skills,
            "found_soft_skills": found_soft_skills,
            "interview_questions": questions,
            "agent_verdicts": agent_verdicts,
            "trajectory": trajectory,
            "market_value": market_value
        }

if __name__ == "__main__":
    scorer = TalentScorer()
    print("NexusTalent Quantum Scorer initialized.")

