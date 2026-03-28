from openai import OpenAI
import json

def run_integrity_guardian(master_resume, ai_generated_bullets, ai_cover_letter, jd, api_key):
    """
    Consolidated Layer 4: Fact-Checker + Interview Coach
    The 'Final Gatekeeper' for data fidelity.
    """
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    prompt = f"""
    ACT AS: A High-Stakes Compliance Auditor and Technical Interviewer.
    
    SOURCE OF TRUTH (Master Resume): {master_resume}
    AI GENERATED CONTENT:
    - Bullets: {ai_generated_bullets}
    - Cover Letter: {ai_cover_letter}
    - Target JD: {jd}

    TASK 1: FACT-CHECK (The Veto)
    Cross-reference the AI content against the Master Resume. Identify any 'Hallucinations' (skills, dates, or titles not in the source).
    
    TASK 2: INTERVIEW PREP
    Based on the verified strengths and the JD requirements, generate 3 'Grilling' technical questions the candidate should prepare for.

    OUTPUT FORMAT (STRICT JSON):
    {{
      "integrity_pass": boolean,
      "hallucination_report": "List discrepancies or 'None'",
      "interview_prep": {{
          "q1": "Behavioral/Technical Question",
          "q2": "Technical Deep-Dive",
          "q3": "JD-Specific Challenge"
      }},
      "final_verdict": "Approved or Requires Revision"
    }}
    """

    try:
        response = client.chat.completions.create(
            model="deepseek-chat", # Tier 1 for Logic/Audit precision
            messages=[
                {"role": "system", "content": "You are a ruthless Fact-Checker. Accuracy is 100% required."},
                {"role": "user", "content": prompt}
            ],
            response_format={'type': 'json_object'}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}
