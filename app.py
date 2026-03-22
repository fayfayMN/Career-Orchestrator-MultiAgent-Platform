import streamlit as st
from langchain_openai import ChatOpenAI

st.set_page_config(page_title="Career Orchestrator", page_icon="🤖")
st.title("🚀 Career Orchestrator: DeepSeek Edition")
st.markdown("Bridging the gap between your resume and the job market.")

# Sidebar for the DeepSeek Key
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

# Updated Multi-Agent Button Logic
if st.button("Analyze Gaps & Build Syllabus"):
    if not deepseek_api_key:
        st.error("Please enter your DeepSeek API Key in the sidebar.")
    elif not resume_text or not jd_text:
        st.warning("Please provide both a resume and a job description.")
    else:
        try:
            llm = ChatOpenAI(
                model_name="deepseek-chat", 
                openai_api_key=deepseek_api_key, 
                openai_api_base="https://api.deepseek.com"
            )
            
            # --- AGENT 1: THE AUDITOR ---
            with st.spinner("Agent 1 (The Auditor) is identifying gaps..."):
                prompt = f"Compare Resume: {resume_text} to JD: {jd_text}. List 3 skill gaps."
                gaps = llm.invoke(prompt).content
                st.subheader("🚩 The Gap Analysis")
                st.write(gaps)
                
            # --- AGENT 2: THE TUTOR ---
            with st.spinner("Agent 2 (The Tutor) is creating your syllabus..."):
                tutor_prompt = f"""
                You are an expert technical instructor. Based on these gaps: {gaps}
                Create a blunt, practical 48-hour rapid upskilling plan to bridge them.
                Include specific resource names (YouTube, documentation, etc.).
                """
                syllabus = llm.invoke(tutor_prompt).content
                st.divider()
                st.subheader("📚 Your 48-Hour Rapid Upskilling Plan")
                st.write(syllabus)
                
        except Exception as e:
            st.error(f"An error occurred: {e}")

# app.py
import streamlit as st
from agents.auditor import perform_audit
from agents.storyteller import draft_star_bullets

st.title("Career Orchestrator: Phase 2")

# 1. Input Section
job_desc = st.text_area("Paste Job Description Here")
uploaded_resume = st.file_uploader("Upload Master Resume (JSON/PDF)")

if st.button("Generate Resilience Narrative"):
    # STEP 1: The Auditor identifies matches and gaps [cite: 187]
    gaps = perform_audit(uploaded_resume, job_desc)
    st.write("### Gap Analysis Complete")
    st.dataframe(gaps)

    # STEP 2: The Storyteller drafts the "Bridge" [cite: 189, 191]
    with st.spinner("Agent 3 is drafting your STAR stories..."):
        new_bullets = draft_star_bullets(uploaded_resume, gaps, job_desc)
        
    st.write("### Your STAR-Method Bullets")
    st.info(new_bullets)
    
    # NEXT STEP: Pass this to Agent 4 (Voice Filter) for refinement [cite: 192]
