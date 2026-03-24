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
except ModuleNotFoundError:
    st.error("Critical: 'agents' folder not found. Check your GitHub directory structure.")
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
    
    doc.add_heading('1. Match Audit & Gaps', level=1)
    doc.add_paragraph(f"Match Score: {res['score']}%")
    doc.add_paragraph(res.get('summary', ''))
    doc.add_paragraph(str(res.get('gaps', '')))

    doc.add_heading('2. Tailored Cover Letter', level=1)
    doc.add_paragraph(res.get('cover_letter', ''))

    doc.add_heading('3. Authentic STAR Bullets', level=1)
    doc.add_paragraph(res.get('narrative', ''))

    doc.add_heading('4. 48-Hour Learning Syllabus', level=1)
    doc.add_paragraph(res.get('syllabus', ''))

    bio = BytesIO()
    doc.save(bio)
    return bio.getvalue()

# --- 4. UI SETUP ---
st.set_page_config(page_title="Career Orchestrator", layout="wide", page_icon="🚀")

if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

with st.sidebar:
    st.title("🚀 Career Orchestrator")
    st.markdown("""
    **Stop wasting time and energy.**
    This Strategy Engine helps you:
    * **Audit** matches.
    * **Build** personas.
    * **Bridge** skill gaps.
    """)
    st.divider()
    st.header("🔑 Credentials")
    api_key = st.text_input("DeepSeek API Key", type="password")
    
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

if st.button("🔍 Step 1: Analyze Match Rate"):
    if not api_key or not resume_input or not jd_input:
        st.warning("Please provide API Key, Resume, and Job Description.")
    else:
        with st.status("🧐 Running JSON-Schema Audit...", expanded=True):
            audit_data = perform_audit(resume_input, jd_input, api_key)
            st.session_state.analysis_results = {
                "gaps": audit_data['gaps'], 
                "score": audit_data['score'],
                "summary": audit_data['summary']
            }
            st.rerun()

# --- 6. CONDITIONAL LOGIC ---
if st.session_state.analysis_results:
    res = st.session_state.analysis_results
    st.divider()
    
    m_col, t_col = st.columns([1, 4])
    m_col.metric("Match Score", f"{res['score']}%")
    t_col.info(f"**The Blunt Truth:** {res.get('summary', 'Audit complete.')}")

    if res['score'] < 60:
        st.error("⚠️ Match rate too low. Bridge these gaps first:")
        st.write(res['gaps'])
    else:
        # STEP 1.5: PERSONA DESIGNER
        with st.expander("👤 Step 1.5: Define Your Professional Persona", expanded=True):
            st.markdown("### Who are you beyond the resume?")
            cp1, cp2 = st.columns(2)
            with cp1:
                traits = st.text_input("Your Core Strengths:", placeholder="e.g., Relentless, Data-Driven")
                weakness = st.text_input("A 'Growth Area':", placeholder="e.g., Perfectionism")
            with cp2:
                p_style = st.selectbox("Your Communication Style:", ["Blunt & Direct", "Empathetic & Story-based", "Technical & Precise"])
                user_writing_sample = st.text_area("Writing DNA:", placeholder="Paste a short bio or intro...")

            if st.button("⚖️ Analyze My Fit"):
                with st.spinner("Analyzing culture fit..."):
                    fit_report = judge_persona_fit(traits, weakness, p_style, jd_input, api_key)
                    st.session_state.analysis_results['persona_fit'] = fit_report
                    st.info(f"**Persona Alignment:** {fit_report}")

        # STEP 2: GENERATE PACKAGE
        if "cover_letter" not in res:
            if st.button("🚀 Step 2: Generate Full Package"):
                with st.status("🛠️ Orchestrating 7-Agent Pipeline...", expanded=True):
                    gap_text = str(res['gaps'])
                    syllabus = generate_syllabus(gap_text, api_key)
                    raw_stories = draft_star_bullets(resume_input, gap_text, jd_input, api_key)
                    
                    # FIXED: Passing variables from the expander above
                    narrative = refine_to_human_voice(raw_stories, traits, user_writing_sample, api_key)
                    
                    verify = run_fact_check(resume_input, narrative, api_key)
                    questions = generate_interview_questions(resume_input, gap_text, api_key)
                    cover = generate_cover_letter(resume_input, jd_input, narrative, api_key)
                    
                    st.session_state.analysis_results.update({
                        "syllabus": syllabus, "narrative": narrative,
                        "verification": verify, "questions": questions, "cover_letter": cover
                    })
                    st.toast("Orchestration Complete!", icon="✅")
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
                st.subheader("👨‍💼 Interview Coach")
                if st.button("🔊 Play Questions"): speak_text(res['questions'])
                st.markdown(res['questions'])
                ans = st.text_area("Draft response:")
                if st.button("Grade Response"):
                    grade = evaluate_answer(res['questions'], ans, api_key)
                    st.success(grade)
            
            st.divider()
            doc_bytes = generate_docx(res)
            st.download_button(label="📥 Download Full Report (.docx)", data=doc_bytes, file_name="Career_Orchestrator.docx")
