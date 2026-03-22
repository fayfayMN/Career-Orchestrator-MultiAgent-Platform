import streamlit as st
import sys
import os
from docx import Document
from io import BytesIO
from agents.fact_checker import run_fact_check

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
except ModuleNotFoundError as e:
    st.error(f"Critical Error: Ensure 'agents' folder is lowercase and has __init__.py. {e}")
    st.stop()

# --- 3. SESSION STATE (The Memory Bank) ---
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

# --- 4. UTILITY: COMPILE FULL REPORT ---
def create_full_report(data):
    doc = Document()
    doc.add_heading('Career Orchestrator: Full Analysis Report', 0)
    
    doc.add_heading('1. Gap Audit', level=1)
    doc.add_paragraph(data['gaps'])
    
    doc.add_heading('2. 48-Hour Upskilling Plan', level=1)
    doc.add_paragraph(data['syllabus'])
    
    doc.add_heading('3. Resilience-Based Narrative (STAR)', level=1)
    doc.add_paragraph(data['narrative'])
    
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
    if st.button("🗑️ Clear All Progress"):
        st.session_state.analysis_results = None
        st.rerun()

# --- 6. INPUT SECTION ---
col1, col2 = st.columns(2)
with col1:
    resume_input = st.text_area("Paste Master Resume:", height=250)
with col2:
    jd_input = st.text_area("Paste Job Description:", height=250)

# --- 7. EXECUTION PIPELINE ---
if st.button("Run Multi-Agent Optimization"):
    if not deepseek_api_key or not resume_input or not jd_input:
        st.warning("Please fill in all fields.")
    else:
        try:
            with st.status("🛠️ Running Agentic Pipeline...", expanded=True) as status:
                # Agent 1: Auditor
                st.write("Agent 1: Identifying Gaps...")
                gaps = perform_audit(resume_input, jd_input, deepseek_api_key)
                
                # Agent 2: Tutor
                st.write("Agent 2: Building Syllabus...")
                syllabus = generate_syllabus(gaps, deepseek_api_key)

                # Agent 3: Storyteller
                st.write("Agent 3: Drafting STAR Narratives...")
                raw_stories = draft_star_bullets(resume_input, gaps, jd_input, deepseek_api_key)
                
                # Agent 4: Voice Filter
                st.write("Agent 4: Humanizing Tone...")
                final_narrative = refine_to_human_voice(raw_stories, deepseek_api_key)
                # Agent 5: fact-checker  ...
                st.write("Agent 5: Running Fact-Check Verification...")
                verification_report = run_fact_check(resume_input, final_narrative, deepseek_api_key)
                
                # SAVE TO PERSISTENT MEMORY
                st.session_state.analysis_results = {
                    "gaps": gaps,
                    "syllabus": syllabus,
                    "narrative": final_narrative,
                    "verification": verification_report, # New field
                    "score": 82
                }
              
                status.update(label="✅ All Agents Finished!", state="complete", expanded=False)
                st.rerun() # Refresh to show results in the persistent layer
                    
        except Exception as e:
            st.error(f"Pipeline Error: {e}")

# --- 8. THE PERSISTENT DISPLAY LAYER ---
# This stays on screen even if the app reruns (e.g., after clicking a button)
if st.session_state.analysis_results:
    res = st.session_state.analysis_results
    
    st.divider()
    st.header(f"📊 Resume-to-JD Match: {res['score']}%")
    st.progress(res['score'] / 100)

    # Organized Tabs for clarity
    t1, t2, t3, t4 = st.tabs(["🚩 Gap Audit", "📚 Syllabus", "🗣️ Final Narrative", "✅ Verification"])
    
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
            st.warning("Verification Warning: Please check the following discrepancies:")
            st.write(res['verification'])
        
        # DOWNLOAD ALL DATA AT ONCE
        full_report = create_full_report(res)
        st.download_button(
            label="📄 Download Full Career Strategy (.docx)",
            data=full_report,
            file_name="Career_Orchestrator_Full_Report.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
