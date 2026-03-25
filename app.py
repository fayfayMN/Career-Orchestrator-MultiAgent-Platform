import streamlit as st
import sys
import os
from io import BytesIO
from gtts import gTTS
from docx import Document

# --- 1. SETUP & PATHS ---
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# --- 2. MODULAR IMPORTS ---
try:
    from agents.auditor import perform_audit
    from agents.tutor import generate_syllabus
    from agents.storyteller import draft_star_bullets
    from agents.voice_filter import refine_to_human_voice, judge_persona_fit
    from agents.fact_checker import run_fact_check
    from agents.interviewer import generate_interview_questions, evaluate_answer
    from agents.cover_letter import generate_cover_letter
except ImportError as e:
    st.error(f"Import Error: {e}. Check your agents/voice_filter.py function arguments.")
    st.stop()

# --- 3. HELPER FUNCTIONS ---
def speak_text(text):
    try:
        tts = gTTS(text=text, lang='en')
        with BytesIO() as f:
            tts.write_to_fp(f)
            st.audio(f, format="audio/mp3")
    except Exception as e:
        st.error(f"Audio Error: {e}")

def generate_docx(res):
    doc = Document()
    doc.add_heading('Career Orchestrator: Professional Analysis', 0)
    for title, key in [('Audit', 'summary'), ('Cover Letter', 'cover_letter'), ('STAR Bullets', 'narrative')]:
        doc.add_heading(title, level=1)
        doc.add_paragraph(str(res.get(key, "N/A")))
    bio = BytesIO()
    doc.save(bio)
    return bio.getvalue()

# --- 4. UI SETUP ---
st.set_page_config(page_title="Career Orchestrator", layout="wide", page_icon="🚀")

if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

# --- SIDEBAR ---
with st.sidebar:
    st.title("🚀 Career Orchestrator")
    st.divider()
    api_key = st.text_input("DeepSeek API Key", type="password")
    
    st.divider()
    st.header("🎯 Strategy Setting")
    # CRITICAL: This variable must exist to be passed to the Voice Filter
    job_level = st.selectbox(
        "Target Job Level:",
        ["Entry/Internship", "Associate/Professional", "Senior/Specialist"],
        help="Adjusts AI 'bluntness' and seniority level."
    )
    
    if st.button("🗑️ Reset Session"):
        st.session_state.analysis_results = None
        st.rerun()

# --- 5. MAIN INTERFACE ---
st.header("🎯 Dynamic Match Engine")
col1, col2 = st.columns(2)
with col1:
    resume_input = st.text_area("Paste Master Resume:", height=200)
with col2:
    jd_input = st.text_area("Paste Job Description:", height=200)

# STEP 1: AUDIT
if st.button("🔍 Step 1: Analyze Match Rate"):
    if not api_key or not resume_input or not jd_input:
        st.warning("Please provide all inputs.")
    else:
        with st.status("🧐 Running Potential-Mapping Audit..."):
            audit_data = perform_audit(resume_input, jd_input, api_key)
            st.session_state.analysis_results = audit_data
            st.rerun()

# --- 6. CONDITIONAL RESULTS ---
if st.session_state.analysis_results:
    res = st.session_state.analysis_results
    st.divider()
    st.metric("Match Score", f"{res['score']}%")
    st.info(f"**The Blunt Truth:** {res.get('summary')}")

    if res['score'] >= 50:
        # STEP 1.5: PERSONA DESIGNER
        with st.expander("👤 Step 1.5: Define Your Professional Persona", expanded=True):
            c1, c2 = st.columns(2)
            with c1:
                traits = st.text_input("Strengths:", placeholder="e.g., Data-Driven, Resilient")
                weakness = st.text_input("Growth Area:", placeholder="e.g., Perfectionism")
            with c2:
                p_style = st.selectbox("Style:", ["Blunt", "Empathetic", "Technical"])
                writing_dna = st.text_area("Writing DNA:", placeholder="Paste a short bio...")

            if st.button("⚖️ Analyze My Fit"):
                fit = judge_persona_fit(traits, weakness, p_style, jd_input, api_key)
                st.session_state.analysis_results['persona_fit'] = fit
                st.info(f"**Persona Alignment:** {fit}")

        # STEP 2: FULL ORCHESTRATION
        if "cover_letter" not in res:
            if st.button("🚀 Step 2: Generate Full Package"):
                with st.status("🛠️ Running 7-Agent Pipeline..."):
                    # 1. Syllabus & Raw Stories
                    syllabus = generate_syllabus
