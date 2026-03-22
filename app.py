import streamlit as st
import sys
import os

# 1. FIX: Force Python to see the agents folder
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# 2. FIX: Unified Imports
try:
    from agents.auditor import perform_audit
    from agents.tutor import generate_syllabus
    from agents.storyteller import draft_star_bullets
except ModuleNotFoundError as e:
    st.error(f"Critical Error: Check folder name and __init__.py. {e}")
    st.stop()

# --- STREAMLIT UI SETUP ---
st.set_page_config(page_title="Career Orchestrator", page_icon="🤖")
st.title("🚀 Career Orchestrator: DeepSeek Edition")
st.markdown("Bridging the gap between your resume and the job market.")

# Sidebar for API Key
with st.sidebar:
    st.header("Settings")
    deepseek_api_key = st.text_input("DeepSeek API Key", type="password")
    st.info("Get your key at platform.deepseek.com")

# Input Section
col1, col2 = st.columns(2)
with col1:
    resume_text = st.text_area("Paste Master Resume:", height=300)
with col2:
    jd_text = st.text_area("Paste Job Description:", height=300)

# --- EXECUTION LOGIC ---
if st.button("Analyze Gaps & Build Narrative"):
    if not deepseek_api_key:
        st.error("Please enter your DeepSeek API Key in the sidebar.")
    elif not resume_text or not jd_text:
        st.warning("Please provide both a resume and a job description.")
    else:
        try:
            # --- PHASE 1: THE AUDITOR (Gap Analysis) ---
            with st.spinner("Agent 1 (The Auditor) is identifying gaps..."):
                # FIXED: Added the required api_key argument
                gaps = perform_audit(resume_text, jd_text, deepseek_api_key)
                st.subheader("🚩 The Gap Analysis")
                st.write(gaps)
            
            # --- PHASE 1.5: THE TUTOR (Learning Syllabus) ---
            with st.divider():
                with st.spinner("Agent 2 (The Tutor) is creating your syllabus..."):
                    syllabus = generate_syllabus(gaps, deepseek_api_key)
                    st.subheader("📚 48-Hour Rapid Upskilling Plan")
                    st.write(syllabus)

            # --- PHASE 2: THE STORYTELLER (STAR Stories) ---
            with st.divider():
                with st.spinner("Agent 3 (The Storyteller) is drafting STAR narratives..."):
                    star_stories = draft_star_bullets(resume_text, gaps, jd_text, deepseek_api_key)
                    st.subheader("✍️ Your Resilience-Based STAR Stories")
                    st.info(star_stories)
                    
        except Exception as e:
            st.error(f"An error occurred during agent execution: {e}")
