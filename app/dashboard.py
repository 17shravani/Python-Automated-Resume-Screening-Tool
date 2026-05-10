import streamlit as st
import requests
import pandas as pd
import json
import time
import plotly.express as px
import plotly.graph_objects as go
import hashlib

# --- ULTRA-PREMIUM CONFIG ---
st.set_page_config(page_title="NexusTalent Quantum AI | Elite Intelligence", layout="wide", page_icon="💎")

# --- CYBER-CORPORATE GLASSMORPHISM CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    :root {
        --primary: #00f2fe;
        --secondary: #4facfe;
        --accent: #f093fb;
        --bg: #0f172a;
        --card-bg: rgba(30, 41, 59, 0.7);
    }

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
        color: #f8fafc;
    }

    .main {
        background: radial-gradient(circle at top right, #1e293b, #0f172a);
        background-attachment: fixed;
    }

    /* Glassmorphic Cards */
    .glass-card {
        background: var(--card-bg);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        border: 1px solid rgba(0, 242, 254, 0.4);
        transform: translateY(-5px);
    }

    /* Neon Metrics */
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(to right, #00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Agent Verdicts */
    .agent-card {
        padding: 1.5rem;
        border-radius: 15px;
        background: rgba(255, 255, 255, 0.03);
        border-left: 5px solid var(--primary);
        margin-bottom: 1rem;
    }

    .agent-name {
        font-weight: 700;
        color: var(--primary);
        font-size: 1.1rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.95);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    .stButton>button {
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        color: #0f172a;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 2rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        width: 100%;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }

    .stButton>button:hover {
        box-shadow: 0 0 20px rgba(0, 242, 254, 0.6);
        transform: scale(1.02);
    }

    /* Animate Background */
    @keyframes glow {
        0% { opacity: 0.3; }
        50% { opacity: 0.6; }
        100% { opacity: 0.3; }
    }
    .bg-glow {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: radial-gradient(circle at 50% 50%, rgba(0, 242, 254, 0.05) 0%, transparent 50%);
        pointer-events: none;
        z-index: -1;
        animation: glow 8s infinite;
    }
    </style>
    <div class="bg-glow"></div>
""", unsafe_allow_html=True)

BASE_URL = "http://localhost:8088"

def main():
    st.sidebar.markdown("<h1 style='text-align: center; color: #00f2fe;'>💎 NEXUSTALENT</h1>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='text-align: center; font-size: 0.8rem; opacity: 0.7;'>QUANTUM AI v2.0 PRO MAX</p>", unsafe_allow_html=True)
    st.sidebar.markdown("---")
    
    blind_mode = st.sidebar.toggle("🕶️ Stealth Anonymizer", value=False)
    
    menu = ["Neural Hub", "JD Architect", "Quantum Screen", "Market Intel"]
    choice = st.sidebar.selectbox("Access Module", menu)

    if choice == "Neural Hub":
        st.markdown("<h1 style='font-size: 3rem;'>Intelligence Overview</h1>", unsafe_allow_html=True)
        st.markdown("Global talent metrics powered by Nexus Engines.")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown('<div class="glass-card"><p>Active Pipelines</p><div class="metric-value">12</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="glass-card"><p>Total Candidates</p><div class="metric-value">458</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown('<div class="glass-card"><p>Avg Match Velocity</p><div class="metric-value">94%</div></div>', unsafe_allow_html=True)

        st.subheader("Live Transmission Feed")
        st.info("System fully operational. Ready for high-impact screening.")

    elif choice == "JD Architect":
        st.markdown("<h1>🎯 JD Neural Architect</h1>", unsafe_allow_html=True)
        with st.form("job_form"):
            title = st.text_input("Strategic Role Title")
            desc = st.text_area("Operational Context (Job Description)")
            skills = st.text_input("Quantum Skill Requirements (Comma separated)")
            exp = st.slider("Minimum Experience Threshold", 0, 20, 2)
            
            submit = st.form_submit_button("Deploy Job Pipeline")
            
            if submit:
                payload = {"title": title, "description": desc, "skills": [s.strip() for s in skills.split(",")], "min_experience": exp}
                try:
                    res = requests.post(f"{BASE_URL}/jobs/create", json=payload)
                    if res.status_code == 200:
                        st.success(f"Pipeline Deployed! ID: {res.json()['job_id']}")
                        st.balloons()
                except:
                    st.error("Neural Connection Failed.")

    elif choice == "Quantum Screen":
        st.markdown("<h1>🔍 Quantum Candidate Screening</h1>", unsafe_allow_html=True)
        job_id = st.text_input("Target Pipeline ID")
        
        if job_id:
            st.markdown("---")
            col_a, col_b = st.columns(2)
            with col_a:
                candidate_name = st.text_input("Candidate Identity")
            with col_b:
                uploaded_file = st.file_uploader("Upload Neural DNA (Resume)", type=["pdf", "docx", "txt"])
            
            if st.button("INITIATE QUANTUM ANALYSIS"):
                if uploaded_file and candidate_name:
                    with st.spinner("Decoding DNA..."):
                        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                        data = {"candidate_name": candidate_name}
                        try:
                            res = requests.post(f"{BASE_URL}/screen/{job_id}", files=files, data=data)
                            if res.status_code == 200:
                                result = res.json()
                                display_name = candidate_name
                                if blind_mode:
                                    display_name = f"AGENT-{hashlib.md5(candidate_name.encode()).hexdigest()[:6].upper()}"
                                
                                st.markdown(f"<h2>Analysis for {display_name}</h2>", unsafe_allow_html=True)
                                
                                # Header Stats
                                m1, m2, m3 = st.columns(3)
                                m1.metric("Quantum Score", f"{result['score']}%")
                                m2.metric("Market Worth", result.get('market_value', 'N/A'))
                                m3.metric("Soft Skills", f"{result['breakdown']['soft_skills_score']}%")

                                # Radar and Agents
                                c1, c2 = st.columns([1, 1])
                                with c1:
                                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                                    bd = result.get('breakdown', {})
                                    categories = ['Semantic', 'Skills', 'Experience', 'Soft Skills']
                                    values = [bd.get('semantic_similarity', 0), bd.get('skill_score', 0), bd.get('experience_score', 0), bd.get('soft_skills_score', 0)]
                                    
                                    fig = go.Figure(data=go.Scatterpolar(r=values + [values[0]], theta=categories + [categories[0]], fill='toself', line_color='#00f2fe'))
                                    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(255,255,255,0.1)"), bgcolor="rgba(0,0,0,0)"), paper_bgcolor="rgba(0,0,0,0)", font_color="white", showlegend=False, margin=dict(l=40, r=40, t=40, b=40))
                                    st.plotly_chart(fig, use_container_width=True)
                                    st.markdown('</div>', unsafe_allow_html=True)

                                with c2:
                                    st.markdown("### AI Decision Panel")
                                    agents = result.get('agent_verdicts', {})
                                    icons = {"Technical Oracle": "🤖", "Strategic Lead": "📈", "Culture Guardian": "⚖️"}
                                    for agent, data in agents.items():
                                        st.markdown(f"""
                                            <div class="agent-card">
                                                <div class="agent-name">{icons.get(agent, '👤')} {agent}</div>
                                                <p style='font-size: 0.9rem; opacity: 0.9;'>{data['verdict']}</p>
                                                <div style='background: rgba(255,255,255,0.1); height: 4px; border-radius: 2px;'>
                                                    <div style='width: {data['score']}%; background: var(--primary); height: 100%; border-radius: 2px;'></div>
                                                </div>
                                            </div>
                                        """, unsafe_allow_html=True)

                                # Trajectory and Roadmap
                                t1, t2 = st.columns(2)
                                with t1:
                                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                                    st.markdown("### 🚀 Career Trajectory")
                                    traj = result.get('trajectory', [])
                                    for i, step in enumerate(traj):
                                        st.markdown(f"**{i+1}. {step}**")
                                        if i < len(traj)-1: st.markdown("↓")
                                    st.markdown('</div>', unsafe_allow_html=True)
                                
                                with t2:
                                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                                    st.markdown("### 🛠️ Quantum Skill Roadmap")
                                    matched = result.get('matched_skills', [])
                                    missing = result.get('missing_skills', [])
                                    st.write(f"✅ **Mastered:** {', '.join(matched[:5])}...")
                                    st.write(f"🚧 **Target Skills:** {', '.join(missing[:5])}...")
                                    st.markdown('</div>', unsafe_allow_html=True)

                        except Exception as e:
                            st.error(f"Analysis Disrupted: {e}")

    elif choice == "Market Intel":
        st.markdown("<h1>📊 Market Intelligence Hub</h1>", unsafe_allow_html=True)
        job_id = st.text_input("Enter Pipeline ID for Rankings")
        
        if job_id:
            if st.button("REVEAL LEADERBOARD"):
                try:
                    res = requests.get(f"{BASE_URL}/rankings/{job_id}")
                    if res.status_code == 200:
                        data = res.json()
                        if data:
                            df = pd.DataFrame(data)
                            if blind_mode:
                                df['name'] = df['name'].apply(lambda x: f"AGENT-{hashlib.md5(x.encode()).hexdigest()[:6].upper()}")
                            
                            fig = px.bar(df, x='name', y='score', color='score', color_continuous_scale='Blues', title="Quantum Rank Distribution")
                            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
                            st.plotly_chart(fig, use_container_width=True)
                            
                            st.dataframe(df[['name', 'score']], use_container_width=True)
                        else:
                            st.info("No neural data found for this pipeline.")
                except:
                    st.error("Intel Feed Disrupted.")

if __name__ == "__main__":
    main()

