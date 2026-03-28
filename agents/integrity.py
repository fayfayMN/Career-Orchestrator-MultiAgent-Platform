import json
from openai import OpenAI

def run_integrity_guardian(master_resume, ai_generated_bullets, ai_cover_letter, jd, api_key):
    """
    Consolidated Layer 4: Fact-Checker + Interview Coach.
    The 'Final Gatekeeper' for data fidelity and interview readiness.
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
    Cross-reference the AI content against the Master Resume. Identify any 'Hallucinations' 
    (skills, dates, or metrics like '1st place' or '70,000 records' that aren't in the source).
    
    TASK 2: INTERVIEW PREP
    Generate 3 'Grilling' technical questions based on the JD and the candidate's specific background:
    1. THE DEEP-DIVE: A tool they claim to know (e.g., Python, SQL).
    2. THE GAP TEST: A challenge involving a skill they are missing from the JD.
    3. THE GRIT CHECK: A STAR-method question about handling 'messy' situations.

    OUTPUT FORMAT (STRICT JSON):
    {{
      "integrity_pass": boolean,
      "hallucination_report": "List discrepancies or 'CLEAN'",
      "interview_questions": {{
          "q1_technical": "string",
          "q2_gap_strategy": "string",
          "q3_grit_behavioral": "string"
      }},
      "final_verdict": "Approved or Requires Revision"
    }}
    """

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a ruthless Fact-Checker. Accuracy is 100% required."},
                {"role": "user", "content": prompt}
            ],
            response_format={'type': 'json_object'}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {
            "integrity_pass": False,
            "hallucination_report": f"Error: {str(e)}",
            "interview_questions": {},
            "final_verdict": "System Error"
        }

def evaluate_interview_voice(question, transcribed_answer, api_key):
    """
    The Evaluator: Grades the user's spoken answer based on the STAR method and Technical Accuracy.
    Used by the Interactive Voice Loop in app.py.
    """
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    prompt = f"""
    ACT AS: A Blunt Technical Interviewer.
    QUESTION: {question}
    CANDIDATE ANSWER: {transcribed_answer}

    RUBRIC:
    1. STAR Method: Did they mention Situation, Task, Action, and a QUANTIFIABLE Result?
    2. Grit: Is the tone blunt and practical (USPS-style grit)?
    3. AI-Slop: Penalize them if they used fluff words like 'synergy' or 'leverage'.
    
    OUTPUT FORMAT (STRICT JSON):
    {{
      "score": "1-10",
      "blunt_feedback": "string",
      "star_breakdown": {{
          "S_T": "string",
          "Action": "string",
          "Result": "string"
      }}
    }}
    """

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a blunt Interview Evaluator. You hate fluff."},
                {"role": "user", "content": prompt}
            ],
            response_format={'type': 'json_object'}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}
