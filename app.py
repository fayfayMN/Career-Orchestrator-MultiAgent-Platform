
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

# 1. Setup the Page (The Professional Look)
st.set_page_config(page_title="Career Orchestrator", page_icon="🤖")
st.title("🚀 Career Orchestrator: Bridge the Gap")
st.markdown("Finding the 'blind spots' in your application using Multi-Agent AI.")

# 2. Sidebar for API Keys (Practical Security)
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    st.info("Your key is used only for this session.")

# 3. Input Section (The Auditor's Data)
col1, col2 = st.columns(2)
with col1:
    resume_text = st.text_area("Paste your Master Resume here:", height=300)
with col2:
    jd_text = st.text_area("Paste the Job Description here:", height=300)

# 4. Agent 1: The Auditor Logic
if st.button("Analyze Gaps"):
    if not openai_api_key:
        st.error("Please add your OpenAI API key to continue.")
    else:
        llm = ChatOpenAI(model_name="gpt-4o", openai_api_key=openai_api_key)
        
        auditor_prompt = f"""
        Compare this Resume: {resume_text} 
        Against this Job Description: {jd_text}
        Identify the 3 most critical 'Gaps' (missing skills or experiences).
        Be blunt and practical.
        """
        
        with st.spinner("The Auditor is analyzing your gaps..."):
            gaps = llm.predict(auditor_prompt)
            st.subheader("🚩 Identified Gaps")
            st.write(gaps)

        # 5. Agent 2: The Tutor (The Bridge)
        st.divider()
        st.subheader("📚 48-Hour Learning Syllabus")
        tutor_prompt = f"Based on these gaps: {gaps}, create a 48-hour rapid upskilling plan."
        syllabi = llm.predict(tutor_prompt)
        st.write(syllabi)
