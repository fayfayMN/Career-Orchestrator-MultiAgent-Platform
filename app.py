import streamlit as st
import pdfplumber
import sys
import os
from io import BytesIO
from docx import Document
from gtts import gTTS
from st_audiorec import st_audiorec

# --- 1. PATH RESILIENCE (Log 05) ---
# CRITICAL: This MUST come before 'from agents import...'
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# --- 2. IMPORT GENERALIZED AGENTS ---
try:
    from agents.strategy_arch import run_strategy_architect
    from agents.ats_architect import run_ats_architect
    from agents.human_narrator import run_human_narrator
    from agents.integrity import run_integrity_guardian
except Exception as e:
    st.error(f"⚠️ App failed to load agents: {e}. Check if agents/__init__.py exists.")
    st.stop()

# --- 3. CONFIGURATION & STATE ---
st.set_page_config(page_title="Career Orchestrator v2.0", layout="wide")

if 'resume_text' not in st.session_state:
    st.session_state.resume_text = ""
if 'final_results' not in st.session_state:
    st.session_state.final_results = None

# --- 4. HELPERS: DOWNLOAD ENGINE ---
def generate_docx_report(company, level, jd, results):
    doc = Document()
    doc.add_heading(f"Strategy Report: {company}", 0)
    
    doc.add_heading("Context & JD Metadata", level=1)
    doc.add_paragraph(f"Target: {company} | Level: {level}")
    
    strat = results.get('strategy', {})
    doc.add_heading("Layer 1: Strategic Audit", level=1)
    doc.add_paragraph(f"Match Score: {strat.get('match_score', 'N/A')}%")
    doc.add_paragraph(strat.get('learning_syllabus', ''))

    doc.add_heading("Layer 2: Optimized ATS Bullets", level=1)
    ats = results.get('ats', {})
    for exp in ats.get('optimized_bullets', []):
        doc.add_heading(exp.get('Role', 'Experience'), level=2)
        for bullet in exp.get('Bullets', []):
            doc.add_paragraph(bullet, style='List Bullet')

    doc.add_heading("Layer 3: Human Narrative", level=1)
    doc.add_paragraph(results.get('narrative', {}).get('cover_letter_narrative', ''))

    bio = BytesIO()
    doc.save(bio)
    return bio.getvalue()

# --- 5. SIDEBAR: PERSONA DISCOVERY ---
with st.sidebar:
    st.header("👤 Persona Discovery")
    api_key = st.text_input("DeepSeek API Key", type="password")
    
    user_strengths = st.text_area("Your Top 3 Strengths", placeholder="e.g., Reliability, Python, Grit")
    user_weaknesses = st.text_area("Gaps/Weaknesses", placeholder="e.g., Public speaking")
    writing_dna = st.selectbox("Writing Style", ["Blunt & Gritty", "Professional", "Academic"])
    
    st.divider()
    st.header("📂 Ingestion")
    uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])

    if uploaded_file and st.button("Parse Resume"):
        with st.spinner("Parsing..."):
            if uploaded_file.type == "application/pdf":
                with pdfplumber.open(uploaded_file) as pdf:
                    st.session_state.resume_text = "\n".join([p.extract_text() for p in pdf.pages if p.extract_text()])
            else:
                doc = Document(uploaded_file)
                st.session_state.resume_text = "\n".join([p.text for p in doc.paragraphs])
        st.success("✅ Resume Loaded")

# --- 6. MAIN UI ---
st.title("🚀 Career Orchestrator: Multi-Agent Platform")
c1, c2 = st.columns(2)

with c1:
    company_name = st.text_input("Target Company", value="Life Time")
    job_level = st.selectbox("Job Level", ["Intern", "Junior", "Senior", "Lead"])
with c2:
    jd_input = st.text_area("Target Job Description", height=150)

# --- 7. GENERALIZED ORCHESTRATION ---
if st.button("🔥 Run Full Optimization") and st.session_state.resume_text:
    if not api_key:
        st.warning("Enter your API Key in the sidebar.")
    else:
        with st.status("Orchestrating Agents...") as status:
            # Phase 1: Strategy & Persona Discovery
            st.write("Phase 1: Discovering Persona...")
            strat = run_strategy_architect(st.session_state.resume_text, jd_input, job_level, company_name, api_key, user_strengths, user_weaknesses, writing_dna)
            
            # Phase 2: ATS keyword mapping
            st.write("Phase 2: Optimizing Keywords...")
            ats = run_ats_architect(st.session_state.resume_text, strat.get('missing_gaps', []), jd_input, strat.get('persona_assessment', ''), job_level, company_name, api_key)
            
            # Phase 3: Human Voice Narrative (Uses the Persona assessment from Phase 1)
            st.write("Phase 3: Crafting Narrative...")
            narrative = run_human_narrator(st.session_state.resume_text, jd_input, strat.get('persona_assessment', 'Technical Professional'), writing_dna, company_name, api_key)
            
            # Phase 4: Final Fact-Check
            st.write("Phase 4: Integrity Audit...")
            integrity = run_integrity_guardian(st.session_state.resume_text, ats, narrative, strat.get('missing_gaps', []), api_key)
            
            st.session_state.final_results = {"strategy": strat, "ats": ats, "narrative": narrative, "integrity": integrity}
            status.update(label="✅ Optimization Complete!", state="complete")

# --- 8. RESULTS DISPLAY ---
if st.session_state.final_results:
    res = st.session_state.final_results
    st.divider()
    
    report_bytes = generate_docx_report(company_name, job_level, jd_input, res)
    st.download_button(label=f"📥 Download {company_name} Strategy Report", data=report_bytes, file_name=f"{company_name}_Report.docx")

    t1, t2, t3 = st.tabs(["📊 Strategy", "📄 ATS Resume", "🎙️ Voice Practice"])
    
    with t1:
        st.metric("Match Score", f"{res['strategy'].get('match_score', 0)}%")
        st.markdown(f"**Persona:** {res['strategy'].get('persona_assessment', 'N/A')}")
        st.markdown(res['strategy'].get('learning_syllabus', ''))
        
    with t2:
        st.json(res['ats']) 
        
    with t3:
        st.subheader("Interactive Interview Grill")
        questions = res['integrity'].get('interview_questions', {})
        if questions:
            q_list = list(questions.values())
            q_selected = st.selectbox("Select Drill:", q_list)
            
            if st.button("📢 Hear Question"):
                tts = gTTS(text=q_selected, lang='en')
                audio_fp = BytesIO()
                tts.write_to_fp(audio_fp)
                st.audio(audio_fp.getvalue(), format='audio/mp3')

            st.write("Record your STAR-method answer:")
            wav_audio_data = st_audiorec()
            if wav_audio_data:
                st.info("Record received. Analyzing...")

   
