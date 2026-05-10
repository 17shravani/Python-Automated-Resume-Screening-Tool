# 💎 TalentFlow AI: Neural Resume Screening Ecosystem

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28.2-FF4B4B.svg)](https://streamlit.io/)
[![spaCy](https://img.shields.io/badge/spaCy-3.7.2-09A3D5.svg)](https://spacy.io/)

**TalentFlow AI** is a production-grade, AI-powered resume screening tool designed to automate the initial recruitment funnel. It uses **Transformer-based Neural Embeddings** and **Named Entity Recognition (NER)** to rank candidates with high precision and explainable logic.

---

## 🚀 Key Features
- **Neural Semantic Matching**: Uses `Sentence-Transformers` to understand context, not just keywords.
- **Automated Entity Extraction**: Extracts Skills, Years of Experience, and Education level using `spaCy`.
- **Hybrid Scoring Engine**: Combines Semantic Similarity (60%), Skill Coverage (30%), and Experience Match (10%).
- **Multi-Format Ingestion**: Supports PDF, DOCX, and TXT files.
- **SaaS-Style Dashboard**: A premium recruiter interface built with Streamlit and custom CSS.
- **Explainable AI**: Provides a detailed breakdown of why a candidate was ranked high or low.
- **Enterprise Ready**: Full FastAPI backend for external integrations.

---

## 🛠️ Tech Stack
- **Backend**: Python, FastAPI, SQLite
- **Intelligence Layer**: spaCy (NLP), Sentence-Transformers (all-MiniLM-L6-v2)
- **Frontend**: Streamlit, Pandas
- **Extraction**: pdfplumber, python-docx
- **Fuzzy Logic**: RapidFuzz

---

## 📂 Project Structure
```text
TalentFlow-AI/
├── src/
│   ├── parser.py        # PDF/DOCX Extraction logic
│   ├── extractor.py     # NLP Entity & Skill extraction
│   └── scorer.py        # Neural Similarity & Weighted scoring
├── app/
│   ├── main.py          # FastAPI Backend (REST API)
│   └── dashboard.py     # Premium Recruiter Dashboard (Streamlit)
├── data/                # Sample data & uploads
├── db/                  # SQLite persistence
├── generate_samples.py  # Simulation script
└── requirements.txt     # Dependency list
```

---

## ⚙️ Installation & Setup

### 1. Clone & Setup Environment
```bash
git clone https://github.com/yourusername/TalentFlow-AI.git
cd TalentFlow-AI
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 3. Generate Simulation Data
```bash
python generate_samples.py
```

---

## 🏃 How to Run

### Step 1: Start the Backend (API)
Open a terminal and run:
```bash
python app/main.py
```
*The API will be available at `http://localhost:8000`*

### Step 2: Start the Dashboard (UI)
Open a **new** terminal and run:
```bash
streamlit run app/dashboard.py
```
*The Dashboard will open in your browser.*

---

## 📊 Virtual Simulation Guide
1. **Create Job**: Go to the "Create Job" tab. Use the generated `python_dev_jd.txt` as a reference.
2. **Screen Resumes**: Upload the sample resumes from `data/resumes/`.
3. **Analyze Results**: View the "Overall Match" and "Skill Breakdown".
4. **Leaderboard**: Check the "Analytics" tab to see the ranked shortlist.

---

## 🎓 Learning Outcomes
- **NLP Pipeline**: Built an end-to-end NLP pipeline for text extraction and information retrieval.
- **Vector Embeddings**: Implemented state-of-the-art neural embeddings for semantic search.
- **Full-Stack ML**: Deployed a model through a production-ready API and UI.
- **Software Engineering**: Applied modular architecture and clean code principles.

---

## 🤝 Interview Preparation
**Q: Why use Transformers instead of just keyword matching?**
*A: Keywords fail to capture context. If a JD asks for "Backend" and a resume says "Server-side developer", keyword matching fails. Transformers understand that these concepts are semantically identical.*

**Q: How do you handle bias in recruitment AI?**
*A: TalentFlow AI focuses on Skills, Experience, and Education. We intentionally omit Personal Identifiable Information (PII) like age, gender, or race from the scoring algorithm to ensure merit-based ranking.*

---
*Created for portfolio demonstration by [Your Name]*
