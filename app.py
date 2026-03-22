from docx import Document
from io import BytesIO

def create_docx(text):
    doc = Document()
    doc.add_heading('Revised Resume Content', 0)
    doc.add_paragraph(text)
    
    # Save to a buffer so Streamlit can download it
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer
    
import streamlit as st
import sys
import os

# 1. SYSTEM SETUP: Force Python to see the agents folder
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# 2. MODULAR IMPORTS
try:
    from agents.auditor import perform_audit
    from agents.tutor import generate_syllabus
    from agents.storyteller import draft_star_bullets
    from agents.voice_filter import refine_to_human_voice
except ModuleNotFoundError as e:
    st.error(f"Critical Error: Check folder name (agents) and __init__.py location. {e}")
    st.stop()

# --- STREAMLIT UI SETUP ---
st.set_page_config(page_title="Career Orchestrator", page_icon="🤖", layout="wide")
st.title("🚀 Career Orchestrator: Multi-Agent Platform")
st.markdown("### Bridging the 'Entry-Level' Gap with Authenticity")

# Sidebar for API Key & Settings
with st.sidebar:
    st.header("🔑 Credentials")
    deepseek_api_key = st.text_input("DeepSeek API Key", type="password")
    st.info("Get your key at platform.deepseek.com")
    st.divider()
    st.write("Current Phase: **Phase 2 (Narrative Engine)**")

# --- INPUT SECTION ---
col1, col2 = st.columns(2)
with col1:
    st.subheader("📄 Your Master Resume")
    resume_text = st.text_area("Paste your background here:", height=300, 
                               placeholder="Include your 3.9 GPA, USPS experience, etc.")
with col2:
    st.subheader("💼 Target Job Description")
    jd_text = st.text_area("Paste the job you want:", height=300,
                           placeholder="Paste the full JD requirements here.")

# --- EXECUTION PIPELINE ---
if st.button("Run Multi-Agent Optimization"):
    if not deepseek_api_key:
        st.error("Please enter your DeepSeek API Key in the sidebar.")
    elif not resume_text or not jd_text:
        st.warning("Please provide both a resume and a job description.")
    else:
        try:
            # PHASE 1: THE AUDITOR (Gap Analysis)
            with st.status("🛠️ Running Agentic Pipeline...", expanded=True) as status:
                
                st.write("Agent 1: The Auditor is identifying gaps...")
                # Call Auditor with all 3 required arguments
                gaps = perform_audit(resume_text, jd_text, deepseek_api_key)
                st.subheader("🚩 The Gap Analysis")
                st.markdown(gaps)
                
                # PHASE 1.5: THE TUTOR (Learning Plan)
                st.write("Agent 2: The Tutor is generating your 48-hour syllabus...")
                syllabus = generate_syllabus(gaps, deepseek_api_key)
                st.subheader("📚 Rapid Upskilling Plan")
                st.markdown(syllabus)

                # PHASE 2: THE STORYTELLER (Drafting)
                st.write("Agent 3: The Storyteller is drafting STAR narratives...")
                # Call Storyteller with all 4 required arguments
                raw_stories = draft_star_bullets(resume_text, gaps, jd_text, deepseek_api_key)
                
                # PHASE 2.5: THE VOICE FILTER (Refining)
                st.write("Agent 4: The Voice Filter is humanizing the tone...")
                final_narrative = refine_to_human_voice(raw_stories, deepseek_api_key)
                
                status.update(label="✅ Optimization Complete!", state="complete", expanded=False)

            # --- FINAL OUTPUT DISPLAY ---
            st.divider()
            st.header("🗣️ Your Authentically Revised Content")
            st.success("This output uses your 'Voice of Resilience' to bridge identified gaps.")
            st.info(final_narrative)
            
            # Download feature for practicality
            st.download_button(
                label="Download Revised Content",
                data=final_narrative,
                file_name="resilience_narrative.txt",
                mime="text/plain"
            )
                    
        except Exception as e:
            st.error(f"Pipeline Error: {e}")
