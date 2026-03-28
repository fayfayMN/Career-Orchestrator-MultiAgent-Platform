import json
from openai import OpenAI

import json
from openai import OpenAI

def run_integrity_guardian(resume_text, ats_data, narrative_data, gaps, api_key):
    """
    Dynamic Layer 4: Generates tailored interview drills and strategic hints.
    """
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    
    # We pass the 'Gaps' and 'Resume' so the AI knows exactly where to push
    prompt = f"""
    ACT AS: A Technical Interviewer & Career Coach.
    TRUTH SOURCE: {resume_text[:1500]}
    IDENTIFIED GAPS: {gaps}

    TASK:
    1. Generate 3 'Grilling' interview questions based on the candidate's technical gaps.
    2. For EACH question, write a 'Strategic Hint' that explicitly tells the candidate how to bridge their 
       specific wins (99.9% USPS accuracy [cite: 2026-03-23] or AGENT.AI #1 Win [cite: 2026-01-09]) 
       to the interviewer's concern.

    OUTPUT FORMAT (STRICT JSON ONLY):
    {{
      "interview_drills": [
        {{
          "question": "The actual tough question text...",
          "strategic_hint": "A STAR-based hint bridging [Resume Win] to [Question Topic]."
        }}
      ],
      "integrity_pass": true
    }}
    """

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "system", "content": "You are a ruthless technical coach. No fluff."},
                      {"role": "user", "content": prompt}],
            response_format={'type': 'json_object'}
        )
        
        content = response.choices[0].message.content.strip()
        
        # Strip Markdown if present
        if content.startswith("```"):
            content = content.split("```")[1].replace("json", "").strip()
            
        return json.loads(content)
        
    except Exception as e:
        # Fallback to ensure the UI doesn't crash if the AI fails
        return {{
            "interview_drills": [
                {{
                    "question": "Tell me about your most complex data project.",
                    "strategic_hint": "Focus on the 70,000-row survey and your cleaning process [cite: 2026-03-28]."
                }}
            ],
            "integrity_pass": False
        }}

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
