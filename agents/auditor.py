# agents/auditor.py
from openai import OpenAI
import json
import re

def perform_audit(resume_text, job_description, api_key):
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    prompt = f"""
    ROLE: High-Precision Technical Recruiter.
    TASK: Perform a 'Deep Audit' of this Resume against the Job Description.
    
    RESUME: {resume_text}
    JOB DESCRIPTION: {job_description}

    OUTPUT FORMAT (STRICT):
    Return ONLY a JSON object with these keys:
    - "score": (An integer from 0-100 representing the match percentage)
    - "matches": (A list of skills found)
    - "gaps": (A list of missing mandatory skills)
    - "summary": (A 2-sentence 'Blunt Truth' assessment)

    TONE: Blunt and factual.
    """

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a technical data auditor. Return only raw JSON."},
            {"role": "user", "content": prompt}
        ],
        response_format={'type': 'json_object'} # Forces DeepSeek to output valid JSON
    )
    
    # Parse the JSON string into a Python Dictionary
    return json.loads(response.choices[0].message.content)
