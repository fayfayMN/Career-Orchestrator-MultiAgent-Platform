import json
from openai import OpenAI

# agents/integrity.py (The Consolidated Version)
def run_integrity_guardian(resume_text, ats_data, narrative_data, gaps, api_key):
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    
    prompt = f"""
    ACT AS: A Senior Auditor & Interview Strategist.
    TRUTH: {resume_text[:1500]}
    GEN-DATA: Bullets: {ats_data} | Letter: {narrative_data}

    TASK:
    1. AUDIT: Identify hallucinations in Gen-Data not supported by Truth.
    2. DRILL: Create 3 interview questions based on {gaps}.
    3. STRATEGIZE: For each question, provide a 'Strategic Hint' bridging their 99.9% USPS accuracy [cite: 2026-03-23] or AGENT.AI win [cite: 2026-01-09] to the problem.

    OUTPUT FORMAT (STRICT JSON):
    {{
      "hallucination_report": "List errors or 'Clean'",
      "integrity_pass": boolean,
      "interview_drills": [
        {{
          "question": "string",
          "strategic_hint": "string"
        }}
      ]
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
    Consolidated Layer 5: The Blunt Coach with Project Isolation.
    Prevents 'Metric Leakage' between USPS, AGENT.AI, and Data Projects.
    """
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    
    prompt = f"""
    QUESTION: {question}
    USER_RAW_ANSWER: {answer}
    
    MANDATE: STRICT PROJECT ISOLATION. 
    - If the question is about the '70,000-row survey', ONLY use facts about Python/SQL/Power BI. 
    - DO NOT mention 'USPS' or 'AGENT.AI' unless the user specifically brought them up in the answer.
    - Hallucinating results (like 99.9% accuracy) into a Data Engineering question is a FATAL ERROR.

    TASK:
    1. BLUNT FEEDBACK: Grade 1-10. Did they actually explain the ETL architecture or just give fluff?
    2. THE REORG (STAR METHOD): 
       - S: Define the specific dataset (Survey vs. Fraud vs. USPS).
       - T: The technical bottleneck (Schema evolution, cleaning, etc.).
       - A: Workhorse verbs (Normalizing, Indexing, Scripting).
       - R: The technical outcome (Validated dashboard, 100% clean schema).
    """
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "system", "content": "You are a Ruthless Technical Coach. You hate project contamination."},
                      {"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Coach Error: {str(e)}"
