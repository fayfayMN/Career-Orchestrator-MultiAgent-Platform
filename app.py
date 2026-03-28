import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# NOW you can import your agents
from agents.strategy_arch import run_strategy_architect
from agents.ats_architect import run_ats_architect
from agents.human_narrator import run_human_narrator
from agents.integrity import run_integrity_guardian
import streamlit as st
import pdfplumber
import asyncio
from io import BytesIO
from docx import Document
from gtts import gTTS
from st_audiorec import st_audiorec

# Import your consolidated agents (Assumes they are in the /agents folder)
from agents.strategy_arch import run_strategy_architect
from agents.ats_architect import run_ats_architect
from agents.human_narrator import run_human_narrator
from agents.integrity import run_integrity_guardian

# --- 1. CONFIGURATION & STATE (Log 05) ---
st.set_page_config(page_title="Career Orchestrator v2.0", layout="wide")

if 'resume_text' not in st.session_state:
    st.session_state.resume_text = ""
if 'final_results' not in st.session_state:
    st.session_state.final_results = None

# --- 2. HELPERS: DOWNLOAD ENGINE (Log 03) ---
def generate_docx_report(company, level, jd, results):
    doc = Document()
    doc.add_heading(f"Career Strategy Report: {company}", 0)
    
    # Metadata Anchor
    doc.add_heading("Target Context & JD Metadata", level=1)
    doc.add_paragraph(f"Organization: {company} | Level: {level}")
    doc.add_paragraph(f"Source JD: {jd[:500]}...")

    # Layer 1: Strategy
    doc.add_heading("Layer 1: Strategic Audit", level=1)
    doc.add_paragraph(f"Match Score: {results['strategy'].get('match_score', 'N/A')}%")
    doc.add_paragraph(results['strategy'].get('learning_syllabus', ''))

    # Layer 2: ATS Resume
    doc.add_heading("Layer 2: Optimized ATS Bullets", level=1)
    for exp in results['ats'].get('ats_experience_bullets', []):
        doc.add_heading(exp.get('Company', 'Experience'), level=2)
        for bullet in exp.get('Bullets', []):
            doc.add_paragraph(bullet, style='List Bullet')

    # Layer 3: Narrative
    doc.add_heading("Layer 3: Human-Grit Narrative", level=1)
    doc.add_paragraph(results['narrative'].get('cover_letter_narrative', ''))

    bio = BytesIO()
    doc.save(bio)
    return bio.getvalue()

# --- 3. SIDEBAR: INGESTION (Log 02) ---
with st.sidebar:
    st.header("📂 Ingestion Layer")
    api_key = st.text_input("DeepSeek API Key", type="password")
    uploaded_file = st.file_uploader("Upload Master Resume", type=["pdf", "docx"])

    if uploaded_file and st.button("Parse Binary Resume"):
        with st.spinner("Parsing..."):
            if uploaded_file.type == "application/pdf":
                with pdfplumber.open(uploaded_file) as pdf:
                    st.session_state.resume_text = "\n".join([p.extract_text() for p in pdf.pages if p.extract_text()])
            else:
                doc = Document(uploaded_file)
                st.session_state.resume_text = "\n".join([p.text for p in doc.paragraphs])
        st.success("✅ Resume Loaded")

# --- 4. MAIN UI: CONTEXT (Log 03) ---
st.title("🚀 Career Orchestrator: Multi-Agent Platform")
c1, c2 = st.columns(2)

with c1:
    company_name = st.text_input("Target Company", value="Life Time")
    job_level = st.selectbox("Job Level", ["Intern", "Junior", "Senior", "Lead"])
with c2:
    jd_input = st.text_area("Target Job Description", height=150)

# --- 5. ORCHESTRATION (Log 01 & 06) ---
if st.button("🔥 Run Full Optimization") and st.session_state.resume_text:
    with st.status("Orchestrating Consolidated Agents...") as status:
        # Layer 1: Strategy
        st.write("Step 1: Auditing Match & Building Syllabus...")
        strat = run_strategy_architect(st.session_state.resume_text, jd_input, job_level, company_name, api_key)
        
        # Layer 2 & 3: Run sequentially for stability (or wrap in asyncio for Log 01)
        st.write("Step 2: Re-Architecting Resume & Human Narrative...")
        ats = run_ats_architect(st.session_state.resume_text, strat['missing_gaps'], jd_input, strat['audit_summary'], job_level, company_name, api_key)
        narrative = run_human_narrator(st.session_state.resume_text, jd_input, strat['audit_summary'], "Blunt/Grit", company_name, api_key)
        
        # Layer 4: Integrity
        st.write("Step 3: Fact-Checking & Interview Prep...")
        integrity = run_integrity_guardian(st.session_state.resume_text, ats, narrative, strat['missing_gaps'], api_key)
        
        st.session_state.final_results = {
            "strategy": strat, "ats": ats, "narrative": narrative, "integrity": integrity
        }
        status.update(label="✅ Optimization Complete!", state="complete")

# --- 6. RESULTS & INTERACTION (Log 07) ---
if st.session_state.final_results:
    res = st.session_state.final_results
    st.divider()
    
    # Context-Aware Download (Log 03)
    report_bytes = generate_docx_report(company_name, job_level, jd_input, res)
    st.download_button(
        label=f"📥 Download {company_name} Strategy Report",
        data=report_bytes,
        file_name=f"{company_name}_Report.docx"
    )

    t1, t2, t3 = st.tabs(["📊 Strategy", "📄 ATS Resume", "🎙️ Voice Practice"])
    
    with t1:
        st.metric("Match Score", f"{res['strategy']['match_score']}%")
        st.markdown(res['strategy']['learning_syllabus'])
        
    with t2:
        st.json(res['ats']) # Showing JSON structure proves the "Auditability"
        
    with t3:
        st.subheader("Interactive Technical Grill")
        questions = res['integrity']['interview_questions']
        q_key = st.selectbox("Select Drill:", list(questions.keys()))
        
        if st.button("📢 Hear Question"):
            tts = gTTS(text=questions[q_key], lang='en')
            audio_fp = BytesIO()
            tts.write_to_fp(audio_fp)
            st.audio(audio_fp.getvalue(), format='audio/mp3')

        st.write("Record your STAR-method answer:")
        wav_audio_data = st_audiorec()
        if wav_audio_data:
            st.info("Record received. Analyzing for STAR-method metrics...")

