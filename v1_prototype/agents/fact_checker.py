# agents/fact_checker.py
from openai import OpenAI

def run_fact_check(original_resume, revised_content, api_key):
    """
    Agent 5: The Fact-Checker.
    Ensures the 'Voice Filter' didn't hallucinate or exaggerate.
    """
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    prompt = f"""
    ROLE: Integrity Auditor.
    TASK: Compare the REVISED CONTENT against the ORIGINAL RESUME.
    
    ORIGINAL DATA: {original_resume}
    REVISED CONTENT: {revised_content}

    CHECK FOR:
    1. DATE MISMATCHES: Did the years of employment or graduation change?
    2. TOOL HALLUCINATIONS: Are there tools mentioned in the revision that are NOT in the original?
    3. METRIC INFLATION: Did a '1st place' become 'International Champion'? 
    
    OUTPUT:
    If everything is 100% accurate, return 'PASSED'.
    If there are errors, list them as 'WARNING: [Issue]'.
    """

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a strict Fact-Checker. You prioritize truth over flowery language."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
