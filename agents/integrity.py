import json
from openai import OpenAI

def run_integrity_guardian(resume_text, ats_data, narrative_data, gaps, api_key, job_level):
    """
    Dynamic Layer 4: Generates level-appropriate interview drills and strategic hints.
    """
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    
    # Dynamic prompt that DISCOVERS the user's best wins
    prompt = f"""
    ACT AS: A Technical Interviewer & Career Coach for {job_level} roles.
    TRUTH SOURCE: {resume_text[:2000]}
    IDENTIFIED GAPS: {gaps}

    TASK:
    1. Generate 3 'Grilling' interview questions tailored to a {job_level} position.
    2. For EACH question, write a 'Strategic Hint'.
       - MANDATE: Identify the candidate's strongest metric or achievement in the 'TRUTH SOURCE' (e.g., accuracy %, rankings, or long tenure).
       - BRIDGE: Tell the candidate exactly how to pivot that specific win to solve the interviewer's concern.

    OUTPUT FORMAT (STRICT JSON ONLY):
    {{
      "interview_drills": [
        {{
          "question": "string",
          "strategic_hint": "string"
        }}
      ],
      "integrity_pass": true
    }}
    """ # <-- Line 70 usually fails here if the closing triple-quotes are missing!

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "system", "content": "You are a ruthless technical coach."},
                      {"role": "user", "content": prompt}],
            response_format={'type': 'json_object'}
        )
        
        content = response.choices[0].message.content.strip()
        
        # Markdown Stripper
        if content.startswith("```"):
            content = content.split("```")[1].replace("json", "").strip()
            
        return json.loads(content)
        
    except Exception as e:
        return {
            "interview_drills": [
                {
                    "question": f"Error loading drills: {str(e)}",
                    "strategic_hint": "Check API connection."
                }
            ],
            "integrity_pass": False
        }

def evaluate_and_reorg_answer(question, answer, api_key):
    """
    Consolidated Layer 5: Feedback without project contamination.
    """
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    
    prompt = f"QUESTION: {question}\nUSER_ANSWER: {answer}\nTASK: Provide a blunt 1-10 grade and re-organize the answer using the STAR method. Focus strictly on technical accuracy."
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "system", "content": "You are a Ruthless Technical Coach."},
                      {"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Coach Error: {str(e)}"
