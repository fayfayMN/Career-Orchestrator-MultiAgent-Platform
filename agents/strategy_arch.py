import json
from openai import OpenAI

def run_strategy_architect(resume, jd, job_level, company_name, api_key, user_strengths, user_weaknesses, writing_dna):
    """
    Synchronized with app.py (8 parameters).
    Analyzes gap between resume and JD using DeepSeek.
    """
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    
    # We use {{ }} for the JSON structure so the f-string doesn't crash
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
    OUTPUT: Return ONLY a JSON object with this EXACT structure:
    {{
      "match_score": 85,
      "persona_assessment": "Short summary of fit",
      "missing_gaps": ["gap1", "gap2"],
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
        
        # Markdown Sanitizer (Log 05)
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
            
        return json.loads(content)
    except Exception as e:
        # Standard Python dictionary for return (Single brackets)
        return {
            "error": str(e), 
            "match_score": 0, 
            "persona_assessment": "Error during LLM processing", 
            "missing_gaps": [], 
            "learning_syllabus": f"Technical Failure: {str(e)}"
        }
