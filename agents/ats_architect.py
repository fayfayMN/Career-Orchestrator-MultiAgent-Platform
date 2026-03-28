import json
from openai import OpenAI

# 1. FIX THE SIGNATURE (Change persona_summary to persona_assessment)
def run_ats_architect(resume_text, gaps, jd, persona_assessment, job_level, company, api_key):
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    
    blacklist = ["synergy", "spearheaded", "passionate", "leverage", "meticulous", "deep-dive"]

    # 2. FIX THE PROMPT (Double the curly braces for the JSON example)
    prompt = f"""
    ACT AS: A Ruthless ATS Optimization Engineer.
    CONTEXT: Target Role at {company} ({job_level}).
    PERSONA: {persona_assessment}
    INPUT: Resume: {resume_text} | Gaps: {gaps} | JD: {jd}
    
    TASK: Rewrite experience into STAR bullets.
    - NO 'corporate ego'. Use 'Workhorse' vocabulary.
    - NO BLACKLIST WORDS: {', '.join(blacklist)}.
    
    OUTPUT FORMAT (STRICT JSON ONLY):
    {{
      "optimized_bullets": [
        {{ "Role": "string", "Bullets": ["list of strings"] }}
      ],
      "persona_alignment_score": "1-10",
      "voice_check_notes": "string"
    }}
    """
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a blunt career engineer."},
                {"role": "user", "content": prompt}
            ],
            response_format={'type': 'json_object'}
        )
        
        content = response.choices[0].message.content.strip()
        
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
            
        return json.loads(content)
        
    except Exception as e:
        return {
            "optimized_bullets": [], 
            "persona_alignment_score": "0", 
            "error": str(e)
        }
