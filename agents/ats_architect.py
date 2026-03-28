# agents/ats_architect.py
import json
from openai import OpenAI

#  Add 'gaps' to the signature
def run_ats_architect(resume_text, jd, job_level, company, gaps, api_key, writing_dna):
    """
    Dynamic Layer 2: The Impact-First Resume Rewriter.
    Updated to handle 7 arguments to match the app.py handshake.
    """
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")


    # The 'Workhorse' Verb List from your guide
    verbs = "Analyzed, Modeled, Evaluated, Engineered, Built, Trained, Optimized, Deployed, Designed, Automated"

    # Inside agents/ats_architect.py
    prompt = f"""
    ... (rest of prompt) ...
    
    OUTPUT FORMAT (STRICT JSON ONLY):
    {{
      "optimized_experience": [
        {{
          "Role": "Job Title",
          "Bullets": ["✅ [Verb] + [Task] + [Tools] + [Impact]"]
        }}
      ],
      "ats_keywords_hit": ["List of keywords from JD found in bullets"],
      "recruiter_scan_verdict": "Blunt 1-sentence assessment of candidate grit."
    }}
    """

      

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "system", "content": "You are a ruthless ATS Engineer. No fluff."},
                      {"role": "user", "content": prompt}],
            response_format={'type': 'json_object'}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}
