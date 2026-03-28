import json
from openai import OpenAI

# 1. FIX THE SIGNATURE (Add the 3 missing parameters)
def run_strategy_architect(resume, jd, job_level, company_name, api_key, user_strengths, user_weaknesses, writing_dna):
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    
    # 2. INJECT PERSONA DATA INTO THE PROMPT
    prompt = f"""
    ACT AS: Senior Recruiter & Strategy Architect at {company_name}.
    
    USER CONTEXT:
    - Target Company: {company_name}
    - Level: {job_level}
    - Writing Style: {writing_dna}
    - Reported Strengths: {user_strengths}
    - Reported Weaknesses: {user_weaknesses}
    
    RESUME: {resume}
    JOB DESCRIPTION: {jd}
    
    TASK: Analyze the gap between the candidate and the JD. 
    OUTPUT: Return ONLY a JSON object with:
    {{
      "match_score": (int 0-100),
      "persona_assessment": "Short summary of how they fit {company_name}",
      "missing_gaps": ["List of skills to address"],
      "learning_syllabus": "Markdown formatted study plan"
    }}
    """
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            response_format={'type': 'json_object'}
        )
        content = response.choices[0].message.content.strip()
        
        # Markdown Sanitizer
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
            
        return json.loads(content)
    except Exception as e:
        # Return a valid dictionary so the next agent doesn't crash
        return {{
            "error": str(e), 
            "match_score": 0, 
            "persona_assessment": "Error in processing", 
            "missing_gaps": [], 
            "learning_syllabus": ""
        }}
