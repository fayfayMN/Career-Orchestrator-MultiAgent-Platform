import json
from openai import OpenAI

def run_integrity_guardian(resume_text, ats_data, narrative_data, gaps, api_key, job_level):
    """
    Dynamic Layer 4: Generates level-appropriate interview drills and strategic hints.
    """
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    
    # Dynamic prompt 
    # agents/integrity.py
import json
from openai import OpenAI

def run_integrity_guardian(resume_text, ats_results, narrative_results, gaps, api_key, job_level):
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    
    # Extract current company from narrative to ensure alignment
    current_company = narrative_results.get('target_company', 'the target company')

    prompt = f"""
    ACT AS: A Technical Interviewer & Career Coach for {job_level} roles.
    TRUTH SOURCE: {resume_text[:2000]}
    IDENTIFIED GAPS: {gaps}
    MANDATE: ZERO-TOLERANCE for industry bleeding. 
    
    CONTEXT:
    - Current Target Company: {current_company}
    - Role Level: {job_level}
    - Optimized Resume Content: {json.dumps(ats_results.get('optimized_experience', []))}
    Tasks:
    For EACH question, write a 'Strategic Hint'.
       - MANDATE: Identify the candidate's strongest metric or achievement in the 'TRUTH SOURCE' (e.g., accuracy %, rankings, or long tenure).
       - BRIDGE: Tell the candidate exactly how to pivot that specific win to solve the interviewer's concern.

    STRICT INSTRUCTIONS:
    1. NO GHOSTING: Do NOT use terminology from healthcare, pharma, or past industries unless they are EXPLICITLY in the current JD.
    2. THE BRIDGE: Create 3 interview questions that challenge the candidate to apply their 'Grit' (e.g., 99.9% USPS accuracy or AGENT.AI wins) to {current_company}'s specific domain.
    3. LEVEL-GATING: Ensure the complexity matches a {job_level} role.
    
    OUTPUT FORMAT (STRICT JSON ONLY):
    {{
      "interview_drills": [
        {{
          "question": "Clear, professional question for {current_company}.",
          "strategic_hint": "STAR-based hint focusing on transferable logic."
        }}
      ]
    }}
    """

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
