import os

def create_sample_files():
    # Ensure directories exist
    os.makedirs("data/resumes", exist_ok=True)
    os.makedirs("data/jd", exist_ok=True)

    # 1. Create a "Perfect Match" Resume (TXT for simplicity, but tool supports PDF/DOCX)
    perfect_resume = """
    JOHN DOE
    Full Stack Python Developer
    
    Summary:
    Innovative Software Engineer with 6 years of experience in Python, AWS, and SQL. 
    Expertise in building scalable FastAPI backends and React frontends.
    
    Skills: Python, SQL, AWS, FastAPI, React, Docker, Kubernetes, Git.
    
    Experience:
    Senior Developer | TechCorp (2018 - Present)
    - Developed microservices using Python and FastAPI.
    - Managed cloud infrastructure on AWS.
    
    Education:
    Master of Science in Computer Science
    """
    with open("data/resumes/john_doe_perfect.txt", "w") as f:
        f.write(perfect_resume)

    # 2. Create an "Average Match" Resume
    avg_resume = """
    JANE SMITH
    Data Analyst
    
    Skills: Python, SQL, Tableau, Excel, Communication.
    
    Experience:
    Analyst | DataSolutions (2 years)
    - Analyzed data using Python and SQL.
    - Created dashboards in Tableau.
    
    Education:
    Bachelor of Commerce
    """
    with open("data/resumes/jane_smith_avg.txt", "w") as f:
        f.write(avg_resume)

    # 3. Create a "Poor Match" Resume
    poor_resume = """
    BOB JOHNSON
    Sales Executive
    
    Experience:
    Sales Manager | RetailPlus (10 years)
    - Managed sales teams.
    - Exceeded targets by 20%.
    
    Skills: Sales, Marketing, Leadership, Communication.
    """
    with open("data/resumes/bob_johnson_poor.txt", "w") as f:
        f.write(poor_resume)

    # 4. Create a Job Description
    jd = """
    JOB TITLE: Senior Python Developer
    
    We are looking for a Senior Python Developer with 5+ years of experience.
    The ideal candidate should be proficient in Python, SQL, and AWS.
    Experience with FastAPI and Docker is a plus.
    
    Requirements:
    - 5+ years of experience in Software Development.
    - Strong knowledge of Python and SQL.
    - Cloud experience with AWS.
    """
    with open("data/jd/python_dev_jd.txt", "w") as f:
        f.write(jd)

    print("Sample files generated in data/ directory!")

if __name__ == "__main__":
    create_sample_files()
