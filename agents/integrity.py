import json
from openai import OpenAI

# --- TASK 1: THE GATEKEEPER ---
def run_integrity_guardian(master_resume, ai_generated_bullets, ai_cover_letter, jd, api_key):
    """
    Consolidated Layer 4: Fact-Checker + Interview Coach.
    Identifies hallucinations and generates the initial drilling questions.
    """
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    prompt = f"""
    ACT AS: A Ruthless Technical Auditor.
    SOURCE OF TRUTH: {master_resume}
    AI CONTENT: Bullets: {ai_generated_bullets} | Letter: {ai_cover_letter}
    
    TASK: Identify any claims not in the Master Resume. 
    Then, generate 3 'Grilling' questions (Technical, Gap Strategy, and Grit-based).
    
    OUTPUT FORMAT (STRICT JSON):
    {{
      "integrity_pass": boolean,
      "hallucination_report": "string",
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
            messages=[{"role": "system", "content": "You are a ruthless Fact-Checker."},
                      {"role": "user", "content": prompt}],
            response_format={'type': 'json_object'}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"integrity_pass": False, "hallucination_report": str(e)}

# --- TASK 2: THE EVALUATOR (JSON DATA) ---
def evaluate_interview_voice(question, transcribed_answer, api_key):
    """
    The Evaluator: Grades the user's spoken answer for the UI metrics.
    """
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    prompt = f"QUESTION: {question}\nANSWER: {transcribed_answer}\nGrade 1-10 on STAR method and USPS-style grit."
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "system", "content": "You are a blunt Interview Evaluator."},
                      {"role": "user", "content": prompt}],
            response_format={'type': 'json_object'}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}

# --- TASK 3: THE REORG COACH (TEXT FEEDBACK) ---
def evaluate_and_reorg_answer(question, answer, api_key):
    """
    Consolidated Layer 5: The Blunt Coach.
    This provides the readable feedback and the 'Perfect' STAR answer.
    """
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    
    prompt = f"""
    QUESTION: {question}
    USER_RAW_ANSWER: {answer}
    
    TASK:
    1. BLUNT FEEDBACK: Grade 1-10 on technical grit.
    2. THE REORG (STAR METHOD): Rewrite their answer into a high-impact narrative.
       - Focus on: 3.9 GPA, #1 AGENT.AI win, and 99.9% USPS accuracy [cite: 2026-03-04, 2026-01-09, 2026-03-23].
       - Use 'Workhorse' verbs (Built, Cleaned, Architected).
    
    STYLE: Blunt, no fluff.
    """
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "system", "content": "You are a blunt Interview Coach. You hate AI-slop."},
                      {"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error connecting to Coach: {str(e)}"
