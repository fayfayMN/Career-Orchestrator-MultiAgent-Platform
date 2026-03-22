import streamlit as st
import sys
import os
import json # Essential for parsing the AI's real score
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
    st.error("Critical: 'agents' folder not found.")
    st.stop()

if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

# --- 3. UI SETUP ---
st.set_page_config(page_title="Career Orchestrator", layout="wide")
st.title("🚀 Career Orchestrator: Dynamic Match Engine")

with st.sidebar:
    st.header("🔑 Credentials")
    api_key = st.text_input("DeepSeek API Key", type="password")
    if st.button("🗑️ Reset Session"):
        st.session_state.analysis_results = None
        st.rerun()

resume_input = st.text_area("Paste Master Resume:", height=150)
jd_input = st.text_area("Paste Job Description:", height=150)

# --- 4. STEP 1: THE REAL AUDIT (PARSING JSON) ---
if st.button("🔍 Step 1: Analyze Match Rate"):
    if not api_key or not resume_input or not jd_input:
        st.warning("Please fill in all fields.")
    else:
        with st.status("🧐 Calculating Real Match Percentage...", expanded=True):
            # Now perform_audit returns a DICTIONARY from Step 1's JSON
            audit_data = perform_audit(resume_input, jd_input, api_key)
            
            # REMOVED: score = 82 (The fake score)
            # ADDED: Using audit_data['score'] from the AI
            st.session_state.analysis_results = {
                "gaps": audit_data['gaps'], 
                "score": audit_data['score'],
                "summary": audit_data['summary']
            }
            st.rerun()

# --- 5. CONDITIONAL DISPLAY & STEP 2 ---
if st.session_state.analysis_results:
    res = st.session_state.analysis_results
    
    st.divider()
    col_a, col_b = st.columns([1, 3])
    with col_a:
        # This will now show the REAL 35% (or whatever the AI calculated)
        st.metric("Match Score", f"{res['score']}%")
    with col_b:
        st.info(f"**The Blunt Truth:** {res.get('summary', 'Audit complete.')}")

    # GATEKEEPER: Prevent Phase 2 if the real score is too low
    if res['score'] < 60:
        st.error("⚠️ Match rate is too low for this role. Use the Audit Gaps to update your resume.")
        st.markdown("### Missing Skills:")
        st.write(res['gaps'])
    else:
        if "cover_letter" not in res:
            if st.button("🚀 Step 2: Generate Full Package"):
                with st.status("🛠️ Running Advanced Agents...", expanded=True):
                    # Passing the specific gaps string to the next agents
                    gap_text = str(res['gaps'])
                    syllabus = generate_syllabus(gap_text, api_key)
                    raw_stories = draft_star_bullets(resume_input, gap_text, jd_input, api_key)
                    narrative = refine_to_human_voice(raw_stories, api_key)
                    verify = run_fact_check(resume_input, narrative, api_key)
                    questions = generate_interview_questions(resume_input, gap_text, api_key)
                    cover = generate_cover_letter(resume_input, jd_input, narrative, api_key)
                    
                    st.session_state.analysis_results.update({
                        "syllabus": syllabus, "narrative": narrative,
                        "verification": verify, "questions": questions, "cover_letter": cover
                    })
                    st.rerun()

        # --- 6. TABBED RESULTS ---
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
                ans = st.text_area("Your Answer:")
                if st.button("Grade Answer"):
                    st.success(evaluate_answer(res['questions'], ans, api_key))
