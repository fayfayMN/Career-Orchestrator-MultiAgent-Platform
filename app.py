import streamlit as st
import sys
import os
from docx import Document
from io import BytesIO
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS

def speak_text(text):
    tts = gTTS(text=text, lang='en')
    with BytesIO() as f:
        tts.write_to_fp(f)
        st.audio(f, format="audio/mp3")

# --- 1. SETUP ---
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    from agents.auditor import perform_audit
    from agents.tutor import generate_syllabus
    from agents.storyteller import draft_star_bullets
    from agents.voice_filter import refine_to_human_voice
    from agents.fact_checker import run_fact_check
    from agents.interviewer import generate_interview_questions, evaluate_answer
except ModuleNotFoundError as e:
    st.error(f"Error: {e}")
    st.stop()

if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

# --- 2. UI ---
st.set_page_config(page_title="Career Orchestrator", layout="wide")
st.title("🚀 Career Orchestrator: Phase 3 (Mock Interview)")

with st.sidebar:
    st.header("🔑 Credentials")
    deepseek_api_key = st.text_input("DeepSeek API Key", type="password")

resume_input = st.text_area("Paste Master Resume:", height=200)
jd_input = st.text_area("Paste Job Description:", height=200)

if st.button("Run Full Agentic Pipeline"):
    with st.status("🛠️ Orchestrating Agents 1-7...", expanded=True) as status:
        gaps = perform_audit(resume_input, jd_input, deepseek_api_key)
        syllabus = generate_syllabus(gaps, deepseek_api_key)
        raw_stories = draft_star_bullets(resume_input, gaps, jd_input, deepseek_api_key)
        final_narrative = refine_to_human_voice(raw_stories, deepseek_api_key)
        verification = run_fact_check(resume_input, final_narrative, deepseek_api_key)
        questions = generate_interview_questions(resume_input, gaps, deepseek_api_key)
        
        st.session_state.analysis_results = {
            "gaps": gaps, "syllabus": syllabus, "narrative": final_narrative,
            "verification": verification, "questions": questions, "score": 82
        }
        status.update(label="✅ Ready for Interview!", state="complete")
        st.rerun()

# --- 3. DISPLAY & INTERVIEW ---
if st.session_state.analysis_results:
    res = st.session_state.analysis_results
    t1, t2, t3, t4, t5 = st.tabs(["🚩 Audit", "📚 Syllabus", "🗣️ Narrative", "✅ Integrity", "🎤 Interview"])
    
    with t1: st.markdown(res['gaps'])
    with t2: st.markdown(res['syllabus'])
    with t3: st.info(res['narrative'])
    with t4: st.write(res['verification'])
    
    with t5:
        st.subheader("👨‍💼 Mock Interview")
        st.markdown(res['questions'])
        st.divider()
        
        st.write("### 🎙️ Record Your Answer")
        # This component handles the microphone and returns text via Whisper
        audio_prompt = mic_recorder(
            start_prompt="Start Recording 🎤",
            stop_prompt="Stop & Convert to Text ⏹️",
            key='recorder'
        )

        # Logic to handle the audio result
        if audio_prompt:
            st.session_state.voice_text = audio_prompt['text']
            st.success("Voice converted successfully!")

        # Show the converted text in the box so you can edit it if needed
        ans = st.text_area("Your STAR Answer (Voice or Type):", 
                           value=st.session_state.get('voice_text', ""))

        if st.button("Submit for Grading"):
            if ans:
                with st.spinner("Agent 7 is evaluating your response..."):
                    feedback = evaluate_answer(res['questions'], ans, deepseek_api_key)
                    st.markdown("### 📊 Evaluator Feedback")
                    st.success(feedback)
            else:
                st.warning("Please record or type an answer first.")
