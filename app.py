import streamlit as st
import sys
import os
from docx import Document
from io import BytesIO
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS

# --- 1. SETUP ---
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

def speak_text(text):
    try:
        tts = gTTS(text=text, lang='en')
        with BytesIO() as f:
            tts.write_to_fp(f)
            st.audio(f, format="audio/mp3")
    except Exception as e:
        st.error(f"Audio Error: {e}")

# --- 2. MODULAR IMPORTS ---
try:
    from agents.auditor import perform_audit
    from agents.tutor import generate_syllabus
    from agents.storyteller import draft_star_bullets
    from agents.voice_filter import refine_to_human_voice
    from agents.fact_checker import run_fact_check
    from agents.interviewer import generate_interview_questions, evaluate_answer
    from agents.cover_letter import generate_cover_letter
except ModuleNotFoundError:
    st.error("Critical: 'agents' folder not found. Ensure it contains __init__.py")
    st.stop()

# Initialize Session State
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

# --- 3. UI SETUP ---
st.set_page_config(page_title="Career Orchestrator", layout="wide")
st.title("🚀 Career Orchestrator: Match-First Logic")

with st.sidebar:
    st.header("🔑 Credentials")
    api_key = st.text_input("DeepSeek API Key", type="password")
    if st.button("🗑️ Reset Session"):
        st.session_state.analysis_results = None
        st.rerun()

resume_input = st.text_area("Paste Master Resume:", height=150)
jd_input = st.text_area("Paste Job Description:", height=150)

# --- 4. STEP 1: THE GATEKEEPER (AUDIT ONLY) ---
if st.button("🔍 Step 1: Analyze Match Rate"):
    if not api_key or not resume_input or not jd_input:
        st.warning("Please fill in all fields.")
    else:
        with st.status("🧐 Running Audit...", expanded=True):
            gaps = perform_audit(resume_input, jd_input, api_key)
            # Logic: Parse a score from Agent 1 or simulate for the gatekeeper
            score = 82 
            st.session_state.analysis_results = {"gaps": gaps, "score": score}
            st.rerun()

# --- 5. CONDITIONAL DISPLAY & STEP 2 ---
if st.session_state.analysis_results:
    res = st.session_state.analysis_results
    
    # Show the Score and Gaps immediately
    st.divider()
    col_a, col_b = st.columns([1, 3])
    with col_a:
        st.metric("Match Score", f"{res['score']}%")
    with col_b:
        st.info(f"**Top Gaps Identified:**\n{res['gaps'][:200]}...")

    # GATEKEEPER: Only allow full generation if score is high enough
    if res['score'] < 60:
        st.error("⚠️ Match too low. Adjust your resume before proceeding.")
    else:
        if "cover_letter" not in res: # Check if we haven't run Phase 2 yet
            if st.button("🚀 Step 2: Generate Full Package (Cover Letter, STAR, Interview)"):
                with st.status("🛠️ Running Agents 2-8...", expanded=True):
                    syllabus = generate_syllabus(res['gaps'], api_key)
                    raw_stories = draft_star_bullets(resume_input, res['gaps'], jd_input, api_key)
                    narrative = refine_to_human_voice(raw_stories, api_key)
                    verify = run_fact_check(resume_input, narrative, api_key)
                    questions = generate_interview_questions(resume_input, res['gaps'], api_key)
                    cover = generate_cover_letter(resume_input, jd_input, narrative, api_key)
                    
                    # Update Memory with everything
                    st.session_state.analysis_results.update({
                        "syllabus": syllabus, "narrative": narrative,
                        "verification": verify, "questions": questions, "cover_letter": cover
                    })
                    st.rerun()

        # --- 6. TABBED RESULTS (Only shows once generated) ---
        if "cover_letter" in res:
            tabs = st.tabs(["🚩 Audit", "📄 Cover Letter", "🗣️ STAR Bullets", "📚 Syllabus", "✅ Integrity", "🎤 Interview"])
            
            with tabs[0]: st.markdown(res['gaps'])
            with tabs[1]: st.write(res['cover_letter'])
            with tabs[2]: st.info(res['narrative'])
            with tabs[3]: st.markdown(res['syllabus'])
            with tabs[4]: st.write(res['verification'])
            with tabs[5]:
                st.subheader("👨‍💼 Interview Coach")
                with st.expander("💡 Pro-Tips"):
                    st.write("Mention ETL, Stakeholders, and STAR structure.")
                if st.button("🔊 Play Questions"): speak_text(res['questions'])
                st.markdown(res['questions'])
                ans = st.text_area("Your Answer:")
                if st.button("Grade Answer"):
                    st.success(evaluate_answer(res['questions'], ans, api_key))
