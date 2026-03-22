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

# ... (Keep your existing imports and setup) ...
from agents.voice_filter import refine_to_human_voice # Ensure this import is added at the top

# inside the 'if st.button("Analyze Gaps & Build Narrative"):' block:
            
            # --- PHASE 2: THE STORYTELLER (STAR Stories) ---
            with st.divider():
                with st.spinner("Agent 3 (The Storyteller) is drafting STAR narratives..."):
                    raw_stories = draft_star_bullets(resume_text, gaps, jd_text, deepseek_api_key)
                    st.subheader("📝 Initial AI Draft (STAR Method)")
                    st.write(raw_stories)
            
            # --- PHASE 2.5: THE VOICE FILTER (Humanizing) ---
            with st.divider():
                with st.spinner("Agent 4 (The Voice Filter) is stripping AI-tone..."):
                    # This agent uses your TRIO/Resilience style guide
                    humanized_narrative = refine_to_human_voice(raw_stories, deepseek_api_key)
                    
                    st.subheader("🗣️ Your Authentically Revised Resume Content")
                    st.success("This version matches your blunt, practical, and resilient voice.")
                    st.info(humanized_narrative)
                    
                    st.download_button(
                        label="Download Revised Content",
                        data=humanized_narrative,
                        file_name="revised_resume_bullets.txt",
                        mime="text/plain"
                    )
