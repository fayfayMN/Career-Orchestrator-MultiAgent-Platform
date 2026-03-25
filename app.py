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
    st.error(f"Critical Sync Error: {e}. Ensure all agent functions match the required arguments.")
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
    for title, key in [('Audit Summary', 'summary'), ('Cover Letter', 'cover_letter'), ('STAR Narrative', 'narrative'), ('Learning Syllabus', 'syllabus')]:
        doc.add_heading(title, level=1)
        doc.add_paragraph(str(res.get(key, "N/A")))
    bio = BytesIO()
    doc.save(bio)
    return bio.getvalue()

# --- 4. UI SETUP ---
st.set_page_config(page_title="Career Orchestrator", layout="wide", page_icon="🚀")

if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

# --- SIDEBAR: MISSION CONTROL ---
with st.sidebar:
    st.title("🚀 Career Orchestrator")
    st.markdown("**Version 2.0: Seniority-Aware Pipeline**")
    st.divider()
    
    st.header("🔑 Credentials")
    api_key = st.text_input("DeepSeek API Key", type="password")
    
    st.divider()
    st.header("🎯 Strategy Setting")
    job_level = st.selectbox(
        "Target Job Level:",
        ["Entry/Internship", "Associate/Professional", "Senior/Specialist"],
        help="This tunes the Storyteller and Voice Filter to the appropriate seniority."
    )
    
    if st.button("🗑️ Reset Session"):
        st.session_state.analysis_results = None
        st.rerun()

# --- 5. MAIN INTERFACE: DATA INGESTION ---
st.header("🎯 Dynamic Match Engine")
col1, col2 = st.columns(2)
with col1:
    resume_input = st.text_area("Paste Master Resume:", height=200)
with col2:
    jd_input = st.text_area("Paste Job Description:", height=200)

# STEP 1: THE AUDIT (GATEKEEPER)
if st.button("🔍 Step 1: Analyze Match Rate"):
    if not api_key or not resume_input or not jd_input:
        st.warning("Please provide API Key, Resume, and Job Description.")
    else:
        with st.status("🧐 Running Potential-Mapping Audit...", expanded=True):
            audit_data = perform_audit(resume_input, jd_input, api_key)
            st.session_state.analysis_results = audit_data
            st.rerun()

# --- 6. THE ORCHESTRATION PIPELINE ---
if st.session_state.analysis_results:
    res = st.session_state.analysis_results
    st.divider()
    
    # Header Metrics
    m_col, t_col = st.columns([1, 4])
    m_col.metric("Match Score", f"{res['score']}%")
    t_col.info(f"**The Blunt Truth:** {res.get('summary')}")

    # Logic Branch: Only proceed if score is viable
    if res['score'] < 50:
        st.error("⚠️ Match rate too low. Bridge these gaps before proceeding:")
        st.write(res['gaps'])
    else:
        # STEP 1.5: PERSONA DESIGNER (CONSULTATION)
        with st.expander("👤 Step 1.5: Define Your Professional Persona", expanded=True):
            st.markdown("### Human-Job Alignment")
            c1, c2 = st.columns(2)
            with c1:
                traits = st.text_input("Top Strengths:", placeholder="e.g., Data-Driven, Resilient")
                weakness = st.text_input("Growth Area:", placeholder="e.g., Perfectionism")
            with c2:
                p_style = st.selectbox("Style:", ["Blunt & Direct", "Empathetic", "Technical"])
                writing_dna = st.text_area("Writing Sample:", placeholder="Paste a short bio to match your voice...")

            if st.button("⚖️ Analyze My Fit"):
                with st.spinner("Judging culture fit..."):
                    fit = judge_persona_fit(traits, weakness, p_style, jd_input, api_key)
                    st.session_state.analysis_results['persona_fit'] = fit
                    st.info(f"**Persona Judgment:** {fit}")

        # STEP 2: FULL PACKAGE GENERATION
        if "cover_letter" not in res:
            if st.button("🚀 Step 2: Generate Full Package"):
                with st.status("🛠️ Running 7-Agent Pipeline...", expanded=True):
                    gaps_text = str(res['gaps'])
                    
                    # 1. Syllabus
                    
                    syllabus = generate_syllabus(gaps_text, job_level, api_key)
                    
                    # 2. THE STORYTELLER (This is for your RESUME bullets)
                    # This stays professional and third-person.
                    resume_bullets = draft_star_bullets(
                        resume_text=resume_input, 
                        gaps=gaps_text, 
                        jd=jd_input, 
                        job_level=job_level, 
                        api_key=api_key
                    )
                    
                    # 3. THE VOICE FILTER (This is ONLY for your COVER LETTER)
                    # This takes the facts and makes them sound like "Feifei Li" speaking.
                    cover_letter_narrative = refine_to_human_voice(
                        draft_text=resume_bullets, 
                        traits=traits, 
                        user_writing_sample=writing_dna, 
                        job_level=job_level, 
                        api_key=api_key
                    )
                    # 4. Verification & Support Agents
                    verify = run_fact_check(resume_input, narrative, api_key)
                    questions = generate_interview_questions(resume_input, gaps_text, api_key)
                    cover = generate_cover_letter(resume_input, jd_input, narrative, api_key)
                    
                    # 5. Commit to State
                    st.session_state.analysis_results.update({
                        "syllabus": syllabus, 
                        "narrative": narrative,
                        "verification": verify, 
                        "questions": questions, 
                        "cover_letter": cover
                    })
                    st.rerun()

        # --- 7. TABBED OUTPUTS ---
        if "cover_letter" in res:
            tabs = st.tabs(["🚩 Audit", "📄 Cover Letter", "🗣️ STAR Bullets", "📚 Syllabus", "✅ Integrity", "🎤 Interview"])
            with tabs[0]: st.write(res['gaps'])
            with tabs[1]: st.write(res['cover_letter'])
            with tabs[2]: st.info(res['narrative'])
            with tabs[3]: st.markdown(res['syllabus'])
            with tabs[4]: st.write(res['verification'])
            with tabs[5]:
                st.subheader("👨‍💼 Interview Simulation")
                if st.button("🔊 Play Questions"): speak_text(res['questions'])
                st.markdown(res['questions'])
                ans = st.text_area("Draft your response here:")
                if st.button("Grade Response"):
                    st.success(evaluate_answer(res['questions'], ans, api_key))
            
            st.divider()
            doc_bytes = generate_docx(res)
            st.download_button(
                label="📥 Download Full Career Package (.docx)",
                data=doc_bytes,
                file_name="Career_Orchestrator_Report.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
