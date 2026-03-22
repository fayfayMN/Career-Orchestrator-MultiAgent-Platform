# agents/auditor.py
from openai import OpenAI

def perform_audit(resume_text, job_description, api_key):
    """
    Agent 1: The Auditor. 
    Compares Resume vs. JD to find the 'Blunt Truth' about skill gaps.
    """
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    prompt = f"""
    ROLE: High-Precision Technical Recruiter.
    TASK: Perform a 'Deep Audit' of this Resume against the Job Description.
    
    RESUME: {resume_text}
    JOB DESCRIPTION: {job_description}

    OUTPUT REQUIREMENTS:
    1. MATCHES: List technical skills the user clearly possesses.
    2. GAPS: List mandatory tools or skills mentioned in the JD that are NOT on the resume.
    3. THE BLUNT TRUTH: Provide a 'Match Percentage'. If it is below 80%, identify the top 2 'Blind Spots'.
    
    TONE: Blunt and factual. No fluff. 
    """

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a blunt Technical Auditor. You identify gaps with 100% honesty."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content
