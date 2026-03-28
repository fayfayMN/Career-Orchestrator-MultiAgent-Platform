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
        MANDATE: Perform a FULL RECONSTRUCTION of the candidate's history. DO NOT skip any roles.
        
        SOURCE DATA: {resume_text}
        TARGET JD: {jd}
    
        TASK:
        1. EXTRACT ALL: Identify every Project, Role, and Volunteer position (USPS, AGENT.AI, MN Tech for Success, etc.) [cite: 2026-03-23, 2026-03-26, 2026-01-09].
        2. PHARMA-PIVOT: Tailor EVERY entry to highlight 'Data Integrity', 'Precision', and 'Standard Operating Procedures' (SOPs) for {company}. [cite: 2026-03-28]
        3. THE FORMULA: 1 Title | Tech Stack line + 4 STAR Bullets (Problem, Method, Result, Impact).
        4. METRIC ENFORCEMENT: You MUST include the 99.9% USPS accuracy, 70k survey rows, and 1st Place wins. [cite: 2026-03-23, 2026-03-28, 2026-01-09]
    
        OUTPUT FORMAT (STRICT JSON ONLY):
        {{
          "optimized_experience": [
            {{
              "Role": "Official Job Title or Project Name",
              "Tech_Stack": "Relevant tools used",
              "Bullets": ["• [STAR Bullet 1]", "• [STAR Bullet 2]", "• [STAR Bullet 3]", "• [STAR Bullet 4]"]
            }}
          ],
          "recruiter_scan_verdict": "...",
          "ats_keywords_hit": []
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

      
