
import streamlit as st
from langchain_openai import ChatOpenAI # DeepSeek uses the OpenAI format

st.set_page_config(page_title="Career Orchestrator", page_icon="🤖")
st.title("🚀 Career Orchestrator: DeepSeek Edition")

with st.sidebar:
    # Rename the input for clarity
    deepseek_api_key = st.text_input("DeepSeek API Key", type="password")

# Input Section
resume_text = st.text_area("Paste Resume:")
jd_text = st.text_area("Paste Job Description:")

if st.button("Analyze with DeepSeek"):
    if not deepseek_api_key:
        st.error("Please add your DeepSeek key.")
    else:
        # We tell LangChain to talk to DeepSeek's server instead of OpenAI's
        llm = ChatOpenAI(
            model_name="deepseek-chat", 
            openai_api_key=deepseek_api_key, 
            openai_api_base="https://api.deepseek.com"
        )
        
        with st.spinner("The Auditor (DeepSeek) is analyzing..."):
            auditor_prompt = f"Resume: {resume_text} \nJD: {jd_text} \nIdentify 3 skill gaps."
            gaps = llm.predict(auditor_prompt)
            st.write(gaps)
