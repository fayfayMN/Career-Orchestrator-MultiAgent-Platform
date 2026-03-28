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
    ACT AS: A Technical Resume Architect.
    MANDATE: Rewrite the 'Projects' and 'Experience' sections to match the High-Signal Entry Level format.
    
    INPUT:
    - Resume: {resume_text[:2000]}
    - Target JD: {jd[:1000]}

    TASK:
    1. For each Project or Role, identify the core 'Tech Stack' (e.g., Python, SQL, Power BI).
    2. Rewrite bullets using the 4-step pattern: Problem, Technical Method, Result, and Visualization/Deployment.
    3. Use 'Workhorse' verbs: Engineered, Normalized, Architected.

    OUTPUT FORMAT (STRICT JSON ONLY):
    {{
      "optimized_experience": [
        {{
          "Role": "Project or Job Title",
          "Tech_Stack": "Python, Pandas, Scikit-learn",
          "Bullets": [
            "• Built/Analyzed [Problem] using [Dataset Size] records.",
            "• Performed [Technical Method/Cleaning] with [Tools].",
            "• Trained/Applied [Algorithms] achieving [Metric] accuracy/impact [cite: 2026-01-09].",
            "• Visualized [Outcome] using [Visualization Tool] to [Stakeholder Benefit]."
          ]
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

      
