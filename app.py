def generate_docx(res):
    doc = Document()
    doc.add_heading('Career Orchestrator: Professional Analysis', 0)
    
    doc.add_heading('1. Match Audit & Gaps', level=1)
    doc.add_paragraph(f"Match Score: {res['score']}%")
    doc.add_paragraph(res['summary'])
    doc.add_paragraph(str(res['gaps']))

    doc.add_heading('2. Tailored Cover Letter', level=1)
    doc.add_paragraph(res['cover_letter'])

    doc.add_heading('3. Authentic STAR Bullets', level=1)
    doc.add_paragraph(res['narrative'])

    doc.add_heading('4. 48-Hour Learning Syllabus', level=1)
    doc.add_paragraph(res['syllabus'])

    # Save to a byte buffer so Streamlit can download it
    bio = BytesIO()
    doc.save(bio)
    return bio.getvalue()
import streamlit as st
import sys
import os
from io import BytesIO
from gtts import gTTS
from agents.voice_filter import refine_to_human_voice, judge_persona_fit

# --- 1. SETUP & PATHS ---
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
    st.error("Critical: 'agents' folder not found. Check your GitHub directory structure.")
    st.stop()

# Initialize Session State
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

# --- 3. UI LAYOUT (SIDEBAR MISSION) ---
st.set_page_config(page_title="Career Orchestrator", layout="wide", page_icon="🚀")

with st.sidebar:
    st.title("🚀 Career Orchestrator")
    st.markdown("""
    **Stop wasting time and energy.**
    This is your personal **Strategy Engine** to:
    * **Audit** matches.
    * **Build** personas.
    * **Bridge** skill gaps.
    * **Coach** for interviews.
    """)
    st.divider()
    
    st.header("🔑 Credentials")
    api_key = st.text_input("DeepSeek API Key", type="password")
    
    st.divider()
    
    st.header("👤 Persona Designer")
    traits = st.text_input("Your Core Strengths:")
    weakness = st.text_input("A 'Growth Area':")
    p_style = st.selectbox("Style:", ["Direct", "Empathetic", "Technical"])
    user_writing_sample = st.text_area("Writing DNA (Paste a bio or intro):", placeholder="Helps the AI match your unique voice...")
    
    if st.button("🗑️ Reset Session"):
        st.session_state.analysis_results = None
        st.rerun()

# --- 4. MAIN INTERFACE ---
st.header("🎯 Dynamic Match Engine")

col1, col2 = st.columns(2)
with col1:
    resume_input = st.text_area("Paste Master Resume:", height=250)
with col2:
    jd_input = st.text_area("Paste Job Description:", height=250)

# --- 5. STEP 1: THE GATEKEEPER AUDIT ---
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

# --- 6. CONDITIONAL RESULTS & STEP 2 ---
if st.session_state.analysis_results:
    res = st.session_state.analysis_results
    
    st.divider()
    m_col, t_col = st.columns([1, 4])
    m_col.metric("Match Score", f"{res['score']}%")
    t_col.info(f"**The Blunt Truth:** {res.get('summary', 'Audit complete.')}")

    # GATEKEEPER BRANCHING
    if res['score'] < 60:
        st.error("⚠️ Match rate is too low. The 'Gatekeeper' has halted the pipeline to save your energy.")
        st.subheader("🚩 Required Skills to Bridge the Gap:")
        st.write(res['gaps'])
    else:
        if "cover_letter" not in res:
            if st.button("🚀 Step 2: Generate Full Package"):
                with st.status("🛠️ Orchestrating 7-Agent Pipeline...", expanded=True):
                    gap_text = str(res['gaps'])
                    
                    # Run Agents
                    syllabus = generate_syllabus(gap_text, api_key)
                    raw_stories = draft_star_bullets(resume_input, gap_text, jd_input, api_key)
                    
                    # UNIVERSAL VOICE FILTER CALL
                    narrative = refine_to_human_voice(raw_stories, user_traits, user_writing_sample, api_key)
                    
                    verify = run_fact_check(resume_input, narrative, api_key)
                    questions = generate_interview_questions(resume_input, gap_text, api_key)
                    cover = generate_cover_letter(resume_input, jd_input, narrative, api_key)
                    
                    st.session_state.analysis_results.update({
                        "syllabus": syllabus, "narrative": narrative,
                        "verification": verify, "questions": questions, "cover_letter": cover
                    })
                    st.toast("Bridge Confirmed: Orchestration Complete!", icon="✅")
                    st.rerun()
        # app.py - After the 60% Match Check
        if res['score'] >= 60:
            with st.expander("👤 Step 1.5: Define Your Professional Persona", expanded=True):
                st.markdown("### Who are you beyond the resume?")
                col_p1, col_p2 = st.columns(2)
                with col_p1:
                    traits = st.text_input("Your Core Strengths:", placeholder="e.g., Relentless, Data-Driven")
                    weakness = st.text_input("A 'Growth Area' or Blind Spot:", placeholder="e.g., Perfectionism, Over-delivering")
                with col_p2:
                    p_style = st.selectbox("Your Communication Style:", ["Blunt & Direct", "Empathetic & Story-based", "Technical & Precise"])
                
                # THE JUDGMENT BUTTON
                if st.button("⚖️ Analyze My Fit"):
                    with st.spinner("Comparing your personality to the job's culture..."):
                        # Call a new function to judge the "Fit"
                        fit_report = judge_persona_fit(traits, weakness, p_style, jd_input, api_key)
                        st.session_state.analysis_results['persona_fit'] = fit_report
                        st.info(f"**Persona Alignment:** {fit_report}")
        # --- 7. TABBED OUTPUTS ---
        if "cover_letter" in res:
            tabs = st.tabs(["🚩 Audit Gaps", "📄 Cover Letter", "🗣️ STAR Bullets", "📚 Syllabus", "✅ Integrity Check", "🎤 Interview Coach"])
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
                    
                # Step 1: Get the grade first
                    grade_result = evaluate_answer(res['questions'], ans, api_key)
                # Step 2: Display it
                    st.success(grade_result)
