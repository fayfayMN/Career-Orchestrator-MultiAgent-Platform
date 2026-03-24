# agents/auditor.py
from openai import OpenAI
import json

def perform_audit(resume_text, job_description, api_key):
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    prompt = f"""
    ROLE: Strategic Talent Architect.
    TASK: Perform a 'Potential Mapping' Audit of this Resume against the Job Description.
    
    RESUME: {resume_text}
    JOB DESCRIPTION: {job_description}

    AUDIT PARAMETERS:
    1. CATEGORY DETECTION: If the JD is for an 'Internship' or 'Junior' role, do NOT penalize for overqualification.
    2. SKILL SUPERSETS: Recognize that advanced DS/ML skills (Python, Modeling) inherently satisfy basic 'Data Analysis/Excel' requirements.
    3. TRANSFERABLE GRIT: Value high-stakes communication (Interpreting) and operational logistics (USPS) as evidence of 'Professional Readiness.'
    4. MATCH SCORE: Base the score on 'Capability to execute' rather than 'Identical job titles.'

    OUTPUT FORMAT (STRICT):
    Return ONLY a JSON object:
    - "score": (Integer 0-100)
    - "matches": (List of skills found)
    - "gaps": (List of missing items - focus ONLY on what prevents them from doing the job)
    - "summary": (A 2-sentence 'Blunt Truth' focusing on how to pivot their high-level skills for this specific role)

    TONE: Practical, encouraging but realistic.
    """

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a strategic career auditor. Return only raw JSON."},
            {"role": "user", "content": prompt}
        ],
        response_format={'type': 'json_object'} 
    )
    
    return json.loads(response.choices[0].message.content)
