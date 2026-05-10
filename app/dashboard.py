import streamlit as st
import requests
import pandas as pd
import json
import time
import plotly.express as px
import plotly.graph_objects as go
import hashlib

# --- PREMIUM STYLING ---
st.set_page_config(page_title="TalentFlow AI | Recruiter Dashboard", layout="wide", page_icon="🚀")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background-color: #f8fafc;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
    }
    
    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    .metric-card {
        text-align: center;
        padding: 1rem;
        background: white;
        border-radius: 10px;
        border-left: 4px solid #6366f1;
    }
    
    h1, h2, h3 {
        color: #1e293b;
    }
    </style>
""", unsafe_allow_html=True)

# --- BACKEND URL ---
BASE_URL = "http://localhost:8000"

def main():
    st.sidebar.title("💎 TalentFlow AI")
    st.sidebar.markdown("---")
    blind_mode = st.sidebar.checkbox("🕶️ Blind Screening Mode", value=False)
    menu = ["Dashboard", "Create Job", "Screen Resumes", "Analytics"]
    choice = st.sidebar.selectbox("Navigate", menu)

    if choice == "Dashboard":
        st.title("Recruiter Overview")
        st.markdown("Monitor candidate pipelines and AI matching in real-time.")
        
        col1, col2, col3 = st.columns(3)
        col1.markdown('<div class="metric-card"><h3>Active Jobs</h3><h2>12</h2></div>', unsafe_allow_html=True)
        col2.markdown('<div class="metric-card"><h3>Candidates</h3><h2>458</h2></div>', unsafe_allow_html=True)
        col3.markdown('<div class="metric-card"><h3>Avg. Score</h3><h2>72%</h2></div>', unsafe_allow_html=True)
        
        st.subheader("Recent Screenings")
        # Sample data if API is not running or empty
        try:
            # Try to fetch some real data if possible (e.g., from first job)
            pass 
        except:
            st.info("Start by creating a job and screening resumes.")

    elif choice == "Create Job":
        st.title("🎯 Create New Job Posting")
        with st.form("job_form"):
            title = st.text_input("Job Title", placeholder="e.g. Senior Python Developer")
            desc = st.text_area("Job Description", placeholder="Describe the role, responsibilities, and context...")
            skills = st.text_input("Required Skills (Comma separated)", placeholder="Python, SQL, AWS...")
            exp = st.number_input("Minimum Experience (Years)", min_value=0, max_value=20, value=2)
            
            submit = st.form_submit_button("Launch Job Pipeline")
            
            if submit:
                payload = {
                    "title": title,
                    "description": desc,
                    "skills": [s.strip() for s in skills.split(",")],
                    "min_experience": exp
                }
                try:
                    res = requests.post(f"{BASE_URL}/jobs/create", json=payload)
                    if res.status_code == 200:
                        st.success(f"Job Created! ID: {res.json()['job_id']}")
                        st.balloons()
                    else:
                        st.error("Failed to connect to Backend API. Is main.py running?")
                except:
                    st.error("Connection Error: Make sure the FastAPI server is running on port 8000.")

    elif choice == "Screen Resumes":
        st.title("🔍 Intelligent Screening")
        
        # Step 1: Select Job
        job_id = st.text_input("Enter Job ID to screen against")
        
        if job_id:
            st.markdown("---")
            candidate_name = st.text_input("Candidate Name")
            uploaded_file = st.file_uploader("Upload Resume (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])
            
            if st.button("Analyze with AI"):
                if uploaded_file and candidate_name:
                    with st.spinner("Neural Engines analyzing resume..."):
                        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                        data = {"candidate_name": candidate_name}
                        try:
                            res = requests.post(f"{BASE_URL}/screen/{job_id}", files=files, data=data)
                            if res.status_code == 200:
                                result = res.json()
                                
                                display_name = candidate_name
                                if blind_mode:
                                    hash_suffix = hashlib.md5(candidate_name.encode()).hexdigest()[:4].upper()
                                    display_name = f"Candidate - {hash_suffix}"
                                    
                                st.success(f"Analysis Complete for {display_name}")
                                
                                # Radar Chart
                                bd = result.get('breakdown', {})
                                categories = ['Semantic Match', 'Skill Match', 'Experience Match', 'Soft Skills']
                                values = [
                                    bd.get('semantic_similarity', 0),
                                    bd.get('skill_score', 0),
                                    bd.get('experience_score', 0),
                                    bd.get('soft_skills_score', 0)
                                ]
                                
                                fig = go.Figure(data=go.Scatterpolar(
                                  r=values + [values[0]],
                                  theta=categories + [categories[0]],
                                  fill='toself',
                                  line_color='#6366f1'
                                ))
                                fig.update_layout(
                                  polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                                  showlegend=False,
                                  margin=dict(l=40, r=40, t=40, b=40)
                                )
                                
                                c1, c2 = st.columns([1, 1])
                                with c1:
                                    st.metric("Overall AI Score", f"{result['score']}%")
                                    st.plotly_chart(fig, use_container_width=True)
                                    
                                with c2:
                                    st.subheader("Gap Analysis")
                                    st.markdown("**✅ Skills Matched:**")
                                    matched = result.get('matched_skills', result.get('extracted_skills', []))
                                    if matched:
                                        for s in matched:
                                            st.markdown(f"- <span style='color:#10b981;font-weight:bold;'>{s}</span>", unsafe_allow_html=True)
                                    else:
                                        st.write("None")
                                        
                                    st.markdown("**❌ Skills Missing (Gaps):**")
                                    missing = result.get('missing_skills', [])
                                    if missing:
                                        for s in missing:
                                            st.markdown(f"- <span style='color:#ef4444;font-weight:bold;'>{s}</span>", unsafe_allow_html=True)
                                    else:
                                        st.write("None! Perfect Match.")
                                        
                                st.markdown("---")
                                with st.expander("🤖 AI Interview Generator"):
                                    questions = result.get('interview_questions', [])
                                    if questions:
                                        for q in questions:
                                            st.info(q)
                                    else:
                                        st.write("No specific questions generated.")
                            else:
                                st.error("Error during screening. Check Job ID.")
                        except:
                            st.error("Connection Error.")
                else:
                    st.warning("Please provide name and file.")

    elif choice == "Analytics":
        st.title("📊 Ranking & Insights")
        job_id = st.text_input("Enter Job ID for Rankings")
        
        if job_id:
            if st.button("Generate Leaderboard"):
                try:
                    res = requests.get(f"{BASE_URL}/rankings/{job_id}")
                    if res.status_code == 200:
                        data = res.json()
                        if data:
                            df = pd.DataFrame(data)
                            if blind_mode:
                                df['name'] = df['name'].apply(lambda x: f"Candidate - {hashlib.md5(x.encode()).hexdigest()[:4].upper()}")
                            st.dataframe(df[['name', 'score']], use_container_width=True)
                            
                            # CSV Export
                            csv = df.to_csv(index=False).encode('utf-8')
                            st.download_button("Download Report (CSV)", csv, "rankings.csv", "text/csv")
                        else:
                            st.info("No candidates screened for this job yet.")
                except:
                    st.error("Connection Error.")

if __name__ == "__main__":
    main()
