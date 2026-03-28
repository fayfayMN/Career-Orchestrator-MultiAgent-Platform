import json
from openai import OpenAI

# agents/strategy_arch.py
import json
from openai import OpenAI

def run_strategy_architect(resume_text, jd, job_level, company, api_key, strengths, weaknesses, writing_dna):
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    
    prompt = f"""
    ACT AS: A Senior Technical Career Strategist.
    MANDATE: STRICT DATA FIDELITY. Build the strategy ONLY from the provided Resume and Persona.
    
    CONTEXT:
    - Candidate Resume Data: {resume_text[:2000]}
    - Stated Strengths: {strengths}
    - Stated Weaknesses: {weaknesses}
    - Target: {company} ({job_level} role)

    TASK: Generate a 7-Day 'Grizzled' Strategy tailored to THIS specific candidate.
    1. IDENTIFY GAPS: Compare the {jd} against the provided Resume. List real technical gaps.
    2. THE SYLLABUS: Provide a day-by-day prep guide to close those gaps.
    3. THE PROJECT: Suggest a 'Proof-of-Concept' project based on a real project found in the candidate's Resume to solve a {company} problem.

    OUTPUT FORMAT (STRICT JSON):
    {{
      "match_score": 0,
      "persona_assessment": "Short blunt summary of the candidate's unique value.",
      "missing_gaps": ["List specific gaps"],
      "learning_syllabus": "## 📅 V1 Strategic 7-Day Sprint\\n- **Day 1-2:** Master [Skill].\\n- **Day 3-4:** Build [Project name based on their resume].\\n- **Day 5-6:** Focus on [Soft skill/Compliance].\\n- **Day 7:** Final Simulation.",
      "strategic_priority": "The #1 thing this specific person needs to prove."
    }}
    """
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            response_format={'type': 'json_object'}
        )
        content = response.choices[0].message.content.strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        return json.loads(content)
    except Exception as e:
        return {"error": str(e), "match_score": 0, "learning_syllabus": "Technical Failure"}
