import spacy
import re
from rapidfuzz import process, fuzz

# Load spaCy model (small version for speed)
try:
    nlp = spacy.load("en_core_web_sm")
except:
    import os
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Industry Skill Database (Expandable)
SKILL_DB = [
    "Python", "Java", "C++", "JavaScript", "SQL", "React", "Node.js", "Django", "Flask",
    "Machine Learning", "Deep Learning", "NLP", "TensorFlow", "PyTorch", "Pandas", "NumPy",
    "AWS", "Azure", "Docker", "Kubernetes", "Git", "Tableau", "Power BI", "Excel",
    "Project Management", "Agile", "Scrum", "Communication", "FastAPI", "Next.js",
    "TypeScript", "Go", "Rust", "Swift", "Kotlin", "MongoDB", "PostgreSQL", "Redis"
]

class EntityExtractor:
    """
    NLP Engine for extracting structured data from unstructured resume text.
    """
    def __init__(self):
        self.skills_db = [s.lower() for s in SKILL_DB]

    def extract_skills(self, text):
        """
        Extracts skills using a hybrid of Tokenization and Fuzzy Matching.
        """
        text_lower = text.lower()
        extracted_skills = set()
        
        # Simple token-based match
        tokens = [token.text.lower() for token in nlp(text_lower)]
        for skill in self.skills_db:
            if skill in text_lower:
                extracted_skills.add(skill.capitalize())
        
        # Fuzzy matching for variations
        for token in tokens:
            if len(token) > 3:
                match = process.extractOne(token, self.skills_db, scorer=fuzz.ratio)
                if match and match[1] > 90:
                    extracted_skills.add(match[0].capitalize())
                    
        return sorted(list(extracted_skills))

    def extract_experience(self, text):
        """
        Extracts years of experience using Regex patterns.
        """
        patterns = [
            r'(\d+)\+?\s*years?',
            r'(\d+)\s*yrs?',
            r'experience\s*of\s*(\d+)\s*years?'
        ]
        years = 0
        for pattern in patterns:
            matches = re.findall(pattern, text.lower())
            for m in matches:
                years = max(years, int(m))
        return years

    def extract_education(self, text):
        """
        Simple extraction for Education levels.
        """
        levels = ["B.Tech", "M.Tech", "B.S", "M.S", "PhD", "Bachelor", "Master", "Degree"]
        for level in levels:
            if level.lower() in text.lower():
                return level
        return "Not Specified"

    def parse_all(self, text):
        return {
            "skills": self.extract_skills(text),
            "experience": self.extract_experience(text),
            "education": self.extract_education(text)
        }

if __name__ == "__main__":
    extractor = EntityExtractor()
    sample_text = "Experienced Python developer with 5 years in AWS and SQL. Master of Science."
    print(extractor.parse_all(sample_text))
