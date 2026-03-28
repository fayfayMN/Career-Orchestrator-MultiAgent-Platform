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

    prompt = f"""
    ACT AS: A Senior Technical Resume Strategist.
    MANDATE: Rewrite the user's experience to pass a 10-second recruiter scan.
    
    INPUT DATA:
    - User Resume: {resume_text[:2000]}
    - Target JD: {jd[:1000]}
    - Persona/DNA: {writing_dna}

    STRICT RULES FOR REWRITING:
    1. FORMULA: Every bullet MUST follow: Action Verb + What You Built + Tools + Measurable Result.
    2. KEYWORD INFILTRATION: Extract the top 5 technical skills from the JD and weave them into the 'Action' or 'Tools' section of the bullets.
    3. PROJECT FOCUS: If the user is a student, prioritize technical 'Projects' over generic work history.
    4. NO HALLUCINATION: Use the user's actual dataset sizes (e.g., 70,000 records) or accuracy scores (e.g., 99.9%) found in the resume. [cite: 2026-03-23]
    5. TITLES: Keep original job titles for background check integrity.

    OUTPUT FORMAT (STRICT JSON ONLY):
    {{
      "optimized_experience": [
        {{
          "Role": "Job Title or Project Name",
          "Bullets": [
            "✅ [Verb] + [Task/Built] + [Tools] + [Impact/Result]",
            "✅ [Verb] + [Task/Built] + [Tools] + [Impact/Result]"
          ]
        }}
      ],
      "ats_keywords_hit": ["List of JD keywords successfully included"],
      "recruiter_scan_verdict": "Blunt 1-sentence assessment of the impact."
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
