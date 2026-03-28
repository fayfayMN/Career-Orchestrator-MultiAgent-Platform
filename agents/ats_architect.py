import json
from openai import OpenAI

def run_ats_architect(resume_text, gaps, jd, persona_summary, job_level, company, api_key):
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    
    # Re-insert the constraints to keep the output blunt and technical
    blacklist = ["synergy", "spearheaded", "passionate", "leverage", "meticulous", "deep-dive"]

    prompt = f"""
    ACT AS: A Ruthless ATS Optimization Engineer & 'Hungry Automator'.
    CONTEXT: Target Role at {company} ({job_level}).
    INPUT: Resume: {resume_text} | Gaps to bridge: {gaps} | JD: {jd}
    
    TASK: Rewrite experience into STAR bullets.
    - NO 'corporate ego'. Use 'Workhorse' vocabulary (e.g., 'fixed' not 'optimized').
    - NO BLACKLIST WORDS: {', '.join(blacklist)}.
    - DATA IS KING: Must include hard metrics from the resume (%, $, #).
    - MAPPING: Prioritize keywords found in the JD.

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
                {"role": "system", "content": "You are a blunt career engineer. You hate fluff and AI-slop."},
                {"role": "user", "content": prompt}
            ],
            response_format={'type': 'json_object'}
        )
        
        content = response.choices[0].message.content.strip()
        
        # Log 05: Markdown Sanitizer (Surgical Extraction)
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
