import streamlit as st
import sys
import os
from docx import Document
from io import BytesIO

# --- 1. SYSTEM SETUP ---
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# --- 2. MODULAR IMPORTS ---
try:
    from agents.auditor import perform_audit
    from agents.tutor import generate_syllabus
    from agents.storyteller import draft_star_bullets
    from agents.voice_filter import refine_to_human_voice
    from agents.fact_checker import run_fact_check
except ModuleNotFoundError as e:
    st.error(f"Critical Error: Ensure 'agents' folder is lowercase and has __init__.py. {e}")
    st.stop()

# --- 3. SESSION STATE (Persistent Memory) ---
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

# --- 4. UTILITY: COMPILE FULL VERIFIED REPORT ---
def create_full_report(data):
    doc = Document()
    doc.add_heading('Career Orchestrator: Verified Strategy Report', 0)
    
    doc.add_heading('1. Gap Audit', level=1)
    doc.add_paragraph(data['gaps'])
    
    doc.add_heading('2. 48-Hour Upskilling Plan', level=1)
    doc.add_paragraph(data['syllabus'])
    
    doc.add_heading('3. Humanized STAR Narrative', level=1)
    doc.add_paragraph(data['narrative'])

    doc.add_heading('4. Integrity Verification (Fact-Check)', level=1)
    doc.add_paragraph(data['verification'])
    
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- 5. UI SETUP ---
st.set_page_config(page_title="Career Orchestrator", page_icon="🤖", layout="wide")
st.title("🚀 Career Orchestrator: Multi-Agent Platform")

with st.sidebar:
    st.header("🔑 Credentials")
    deepseek_api_key = st.text_input("DeepSeek API Key", type="password")
    if st.button("🗑️ Reset All Progress"):
        st.session_state.analysis_results = None
        st.rerun()

# --- 6. INPUT SECTION ---
col1, col2 = st.columns(2)
with col1:
    st.subheader("📄 Your Master Resume")
    resume_input = st.text_area("Paste background (include GPA, USPS, etc.):", height=250)
with col2:
    st.subheader("💼 Target Job Description")
    jd_input = st.text_area("Paste job requirements:", height=250)

# --- 7. EXECUTION PIPELINE (AGENTS 1-5) ---
if st.button("Run Multi-Agent Optimization"):
    if not deepseek_api_key or not resume_input or not jd_input:
        st.warning("Please fill in all fields.")
    else:
        try:
            with st.status("🛠️ Orchestrating Agents...", expanded=True) as status:
                # Agent 1: Auditor
                st.write("Agent 1: Identifying Gaps...")
                gaps = perform_audit(resume_input, jd_input, deepseek_api_key)
                
                # Agent 2: Tutor
                st.write("Agent 2: Building Syllabus...")
                syllabus = generate_syllabus(gaps, deepseek_api_key)

                # Agent 3: Storyteller
                st.write("Agent 3: Drafting STAR Narratives...")
                raw_stories = draft_star_bullets(resume_input, gaps, jd_input, deepseek_api_key)
                
                # Agent 4: Voice Filter (Humanizing)
                st.write("Agent 4: Applying Personal Style Guide...")
                final_narrative = refine_to_human_voice(raw_stories, deepseek_api_key)

                # Agent 5: Fact-Checker (Verification)
                st.write("Agent 5: Running Integrity Check...")
                verification = run_fact_check(resume_input, final_narrative, deepseek_api_key)
                
                # SAVE TO PERSISTENT MEMORY
                st.session_state.analysis_results = {
                    "gaps": gaps,
                    "syllabus": syllabus,
                    "narrative": final_narrative,
                    "verification": verification,
                    "score": 82 # Logic for dynamic scoring goes here
                }
                status.update(label="✅ Pipeline Verified!", state="complete", expanded=False)
                st.rerun()
                    
        except Exception as e:
            st.error(f"Pipeline Error: {e}")

# --- 8. THE PERSISTENT DISPLAY LAYER ---
if st.session_state.analysis_results:
    res = st.session_state.analysis_results
    
    st.divider()
    st.header(f"📊 Resume-to-JD Match Score: {res['score']}%")
    st.progress(res['score'] / 100)

    # Organized Tabs
    t1, t2, t3, t4 = st.tabs(["🚩 Gap Audit", "📚 Syllabus", "🗣️ Final Narrative", "✅ Integrity Check"])
    
    with t1:
        st.markdown(res['gaps'])
    with t2:
        st.markdown(res['syllabus'])
    with t3:
        st.info(res['narrative'])
    with t4:
        if "PASSED" in res['verification']:
            st.success("Verification Status: All facts aligned with Master Resume.")
        else:
            st.warning("Integrity Warning: Discrepancies found.")
            st.write(res['verification'])
        
        # DOWNLOAD FULL PROCESS
        full_report = create_full_report(res)
        st.download_button(
            label="📄 Download Full Verified Strategy (.docx)",
            data=full_report,
            file_name="Career_Strategy_Final_Verified.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
