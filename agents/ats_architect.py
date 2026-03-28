# agents/ats_architect.py
import json
from openai import OpenAI

#  Add 'gaps' to the signature
# agents/ats_architect.py

def run_ats_architect(resume_text, jd, job_level, company, gaps, api_key, writing_dna):
    # This matches the 7-item call from app.py
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    
    """
    Dynamic Layer 2: The Impact-First Resume Rewriter.
    Updated to handle 7 arguments to match the app.py handshake.
    """
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")


    # The 'Workhorse' Verb List from your guide
    verbs = "Analyzed, Modeled, Evaluated, Engineered, Built, Trained, Optimized, Deployed, Designed, Automated"

    prompt = f"""
    ACT AS: A Senior Technical Resume Architect.
    MANDATE: Perform a COMPLETE RECONSTRUCTION of the candidate's history.
    
    INSTRUCTIONS:
    1. DISCOVERY: Identify EVERY distinct work experience, project, and volunteer block in: {resume_text}. Do not truncate.
    2. THE PIVOT: Tailor EVERY block to the needs of {company} ({job_level}).
       - If {company} values 'Data Integrity', find evidence of precision in every role. [cite: 2026-03-28]
       - If they value 'Automation', find where the candidate improved workflows.
    3. THE FORMULA (FOR ALL): 
       - Header: **Role Title** | [Tech Stack/Tools]
       - 4 Bullets: Problem -> Technical Method -> Result -> Business/Safety Impact.
    4. METRIC EXTRACTION: Search the resume for every possible number (%, $, row counts, rankings) and embed them into the Result bullets.

    OUTPUT FORMAT (STRICT JSON ONLY):
    {{
      "optimized_experience": [
        {{
          "Role": "Title found in resume",
          "Tech_Stack": "Tools identified for this specific block",
          "Bullets": ["• [Bullet 1]", "• [Bullet 2]", "• [Bullet 3]", "• [Bullet 4]"]
        }}
      ],
      "recruiter_scan_verdict": "Blunt 1-sentence assessment of candidate's grit and technical fit.",
      "ats_keywords_hit": ["List of keywords from the JD found and included"]
    }}
    """
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            response_format={'type': 'json_object'}
        )
        content = response.choices[0].message.content.strip()
        
        # MANDATORY: Strip Markdown backticks that break json.loads()
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
            content = content.split("```")[0].strip()
            
        return json.loads(content)
    except Exception as e:
        # Returning a structured error helps the UI tell you WHAT went wrong
        return {
            "optimized_experience": [],
            "recruiter_scan_verdict": f"Error: {str(e)}",
            "ats_keywords_hit": []
        }

      
