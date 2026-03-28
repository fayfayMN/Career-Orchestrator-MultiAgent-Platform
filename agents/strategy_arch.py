import json
from openai import OpenAI

def run_strategy_architect(resume, jd, job_level, company_name, api_key, user_strengths, user_weaknesses, writing_dna):
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    
    # FIX 1: Doubled curly braces in the prompt so Python doesn't crash
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
    OUTPUT: Return ONLY a JSON object with this structure:
    {{
      "match_score": 85,
      "persona_assessment": "summary",
      "missing_gaps": ["gap1", "gap2"],
      "learning_syllabus": "markdown plan"
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
        # FIX 2: Single curly braces for the actual Python return
        return {
            "error": str(e), 
            "match_score": 0, 
            "persona_assessment": "Error in processing", 
            "missing_gaps": [], 
            "learning_syllabus": f"Failed to generate: {str(e)}"
        }
