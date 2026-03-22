import streamlit as st
import sys
import os
from docx import Document
from io import BytesIO
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS

# --- 1. SETUP & UTILITIES ---
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

def speak_text(text):
    tts = gTTS(text=text, lang='en')
    with BytesIO() as f:
        tts.write_to_fp(f)
        st.audio(f, format="audio/mp3")

def create_full_report(data):
    doc = Document()
    doc.add_heading('Career Orchestrator: Full Verified Suite', 0)
    sections = [
        ('1. Cover Letter', data.get('cover_letter', 'N/A')),
        ('2. Resume Bullets (STAR)', data['narrative']),
        ('3. Gap Audit', data['gaps']),
        ('4. Upskilling Plan', data['syllabus']),
        ('5. Integrity Check', data['verification'])
    ]
    for title, content in sections:
        doc.add_heading(title, level=1)
        doc.add_paragraph(content)
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- 2. MODULAR IMPORTS ---
try:
    from agents.auditor import perform_audit
    from agents.tutor import generate_syllabus
    from agents.storyteller import draft_star_bullets
    from agents.voice_filter import refine_to_human_voice
    from agents.fact_checker import run_fact_check
    from agents.interviewer import generate_interview_questions, evaluate_answer
    from agents.cover_letter import generate_cover_letter
except ModuleNotFoundError as e:
    st.error(f"Error: {e}")
    st.stop()

if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

# --- 3. UI ---
st.set_page_config(page_title="Career Orchestrator", layout="wide")
st.title("🚀 Career Orchestrator: Complete Multi-Agent Suite")

with st.sidebar:
    st.header("🔑 Credentials")
    deepseek_api_key = st.text_input("DeepSeek API Key", type="password")
    if st.button("Reset Session"):
        st.session_state.analysis_results = None
        st.rerun()

resume_input = st.text_area("Paste Master Resume:", height=200)
jd_input = st.text_area("Paste Job Description:", height=200)

# --- 4. EXECUTION ---
if st.button("Generate Full Career Suite"):
    with st.status("🛠️ Running Agents 1-8...", expanded=True) as status:
        gaps = perform_audit(resume_input, jd_input, deepseek_api_key)
        syllabus = generate_syllabus(gaps, deepseek_api_key)
        raw_stories = draft_star_bullets(resume_input, gaps, jd_input, deepseek_api_key)
        final_narrative = refine_to_human_voice(raw_stories, deepseek_api_key)
        verification = run_fact_check(resume_input, final_narrative, deepseek_api_key)
        questions = generate_interview_questions(resume_input, gaps, deepseek_api_key)
        # NEW: Cover Letter Agent
        cover_letter = generate_cover_letter(resume_input, jd_input, final_narrative, deepseek_api_key)
        
        st.session_state.analysis_results = {
            "gaps": gaps, "syllabus": syllabus, "narrative": final_narrative,
            "verification": verification, "questions": questions, 
            "cover_letter": cover_letter, "score": 82
        }
        status.update(label="✅ All Artifacts Ready!", state="complete")
        st.rerun()

# --- 5. DISPLAY ---
if st.session_state.analysis_results:
    res = st.session_state.analysis_results
    tabs = st.tabs(["📄 Cover Letter", "🗣️ Resume Bullets", "🚩 Audit", "📚 Syllabus", "✅ Integrity", "🎤 Interview"])
    
    with tabs[0]: 
        st.subheader("Professional Cover Letter")
        st.write(res['cover_letter'])
    with tabs[1]: st.info(res['narrative'])
    with tabs[2]: st.markdown(res['gaps'])
    with tabs[3]: st.markdown(res['syllabus'])
    with tabs[4]: st.write(res['verification'])
    
    with tabs[5]:
        st.subheader("Mock Interview")
        if st.button("🔊 Read Questions"): speak_text(res['questions'])
        st.markdown(res['questions'])
        ans = st.text_area("Your Answer:")
        if st.button("Grade Answer"):
            st.success(evaluate_answer(res['questions'], ans, deepseek_api_key))
            
    # Final Action
    st.divider()
    full_doc = create_full_report(res)
    st.download_button("📂 Download Full Career Package (.docx)", data=full_doc, file_name="Complete_Application_Package.docx")
