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
    st.error("Critical: 'agents' folder not found. Please verify your GitHub structure.")
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
    sections = [
        ('1. Match Audit', 'summary'),
        ('2. Cover Letter', 'cover_letter'),
        ('3. STAR Bullets', 'narrative'),
        ('4. Learning Syllabus', 'syllabus')
    ]
    for title, key in sections:
        doc.add_heading(title, level=1)
        doc.add_paragraph(str(res.get(key, "Not generated.")))
    bio = BytesIO()
    doc.save(bio)
    return bio.getvalue()

# --- 4. UI SETUP ---
st.set_page_config(page_title="Career Orchestrator", layout="wide", page_icon="🚀")

if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

# --- SIDEBAR: MISSION & SETTINGS ---
with st.sidebar:
    st.title("🚀 Career Orchestrator")
    st.markdown("**Your Strategy Engine** for finding blind spots and bridging gaps.")
    st.divider()
    
    st.header("🔑 Credentials")
    api_key = st.text_input("DeepSeek API Key", type="password")
    
    st.divider()
    st.header("🎯 Strategy Setting")
    job_level = st.selectbox(
        "Target Job Level:",
        ["Entry/Internship", "Associate/Professional", "Senior/Specialist"],
        help="Tunes the Auditor and Voice Filter to match the seniority of the role."
    )
    
    if st.button("🗑️ Reset Session"):
        st.session_state.analysis_results = None
        st.rerun()

# --- 5. MAIN INTERFACE: INPUTS ---
st.header("🎯 Dynamic Match Engine")
col_in1, col_in2 = st.columns(2)
with col_in1:
    resume_input = st.text_area("Paste Master Resume:", height=200)
with col_in2:
    jd_input = st.text_area("Paste Job Description:", height=200)

# --- STEP 1: THE AUDIT ---
if st.button("🔍 Step 1: Analyze Match Rate"):
    if not api_key or not resume_input or not jd_input:
        st.warning("All fields (API Key, Resume, JD) are required.")
    else:
        with st.status("🧐 Running Potential-Mapping Audit...", expanded=True):
            # Pass job_level to the audit if you've updated auditor.py to accept it
            audit_data = perform_audit(resume_input, jd_input, api_key)
            st.session_state.analysis_results = {
                "gaps": audit_data['gaps'], 
                "score": audit_data['score'],
                "summary": audit_data['summary']
            }
            st.rerun()

# --- 6. CONDITIONAL WORKFLOW ---
if st.session_state.analysis_results:
    res = st.session_state.analysis_results
    st.divider()
    
    # METRIC DISPLAY
    m_col, t_col = st.columns([1, 4])
    m_col.metric("Match Score", f"{res['score']}%")
    t_col.info(f"**Audit Assessment:** {res.get('summary')}")

    # GATEKEEPER LOGIC (Strictness based on Job Level could go here)
    if res['score'] < 50: # Lowered threshold slightly for 'Potential Mapping'
        st.error("⚠️ Match rate is critically low. Focus on these gaps:")
        st.write(res['gaps'])
    else:
        # STEP 1.5: PERSONA CONSULTATION
        with st.expander("👤 Step 1.5: Define Your Professional Persona", expanded=True):
            st.markdown("### Human-Job Alignment")
            cp1, cp2 = st.columns(2)
            with cp1:
                traits = st.text_input("Top 3 Strengths:", placeholder="e.g., Relentless, Systematic")
                weakness = st.text_input("Growth Area:", placeholder="e.g., Perfectionism")
            with cp2:
                p_style = st.selectbox("Comms Style:", ["Blunt & Direct", "Empathetic", "Technical"])
                writing_dna = st.text_area("Writing Sample:", placeholder="Paste a bio to match your voice...")

            if st.button("⚖️ Analyze My Fit"):
                with st.spinner("Judging culture fit..."):
                    fit = judge_persona_fit(traits, weakness, p_style, jd_input, api_key)
                    st.session_state.analysis_results['persona_fit'] = fit
                    st.info(f"**Persona Judgment:** {fit}")

        # STEP 2: ORCHESTRATION
        if "cover_letter" not in res:
            if st.button("🚀 Step 2: Generate Full Package"):
                with st.status("🛠️ Running 7-Agent Pipeline...", expanded=True):
                    gaps = str(res['gaps'])
                    
                    # Run Pipeline
                    syllabus = generate_syllabus(gaps, api_key)
                    stories = draft_star_bullets(resume_input, gaps, jd_input, api_key)
                    
                    # Incorporate Job Level into the Voice Filter
                   
                  # Step 2: Running the Voice Filter
                    narrative = refine_to_human_voice(
                        draft_text=stories, 
                        traits=traits, 
                        user_writing_sample=writing_dna, 
                        job_level=job_level,  # <-- THIS IS LIKELY THE MISSING LINE
                        api_key=api_key
                    )
                                        
                    verify = run_fact_check(resume_input, narrative, api_key)
                    qs = generate_interview_questions(resume_input, gaps, api_key)
                    cover = generate_cover_letter(resume_input, jd_input, narrative, api_key)
                    
                    st.session_state.analysis_results.update({
                        "syllabus": syllabus, "narrative": narrative,
                        "verification": verify, "questions": qs, "cover_letter": cover
                    })
                    st.rerun()

        # --- 7. RESULTS TABS ---
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
                ans = st.text_area("Your Response:")
                if st.button("Grade Answer"):
                    st.success(evaluate_answer(res['questions'], ans, api_key))
            
            st.divider()
            doc = generate_docx(res)
            st.download_button("📥 Download Career Report (.docx)", data=doc, file_name="Career_Report.docx")
