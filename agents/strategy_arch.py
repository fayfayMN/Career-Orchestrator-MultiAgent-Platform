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

    TASK: Generate a 7-Day 'Grizzled' Strategic Syllabus for {company}.
    
    INSTRUCTIONS:
    1. GAPS: Identify 3 technical gaps based on the {jd}.
    2. SYLLABUS: Create a Day 1-7 roadmap. 
       - MUST include specific resources (e.g., 'Metropolitan State Library', 'SQLZoo', 'Python Docs').
       - MUST include 1 'Proof-of-Concept' project based on their 70,000-row survey or AGENT.AI win [cite: 2026-01-09].
    3. RIGOR: Ensure 'Day 5-6' focuses on bridging their 99.9% USPS accuracy to Data Integrity [cite: 2026-03-23].

    OUTPUT FORMAT (STRICT JSON ONLY):
    {{
      "match_score": 88,
      "persona_assessment": "Short blunt assessment of their operational grit.",
      "missing_gaps": ["List specific gaps"],
      "learning_syllabus": "## 📅 V1 Strategic 7-Day Sprint\\n\\n- **Day 1-2 (Technical Foundation):** Master [Skill]. **Resource:** [Specific Resource/Link].\\n\\n- **Day 3-4 (The Build):** Project: '[Project Name]'. Task: Re-architect your [Resume Project] to solve [Company Problem].\\n\\n- **Day 5-6 (Operational Rigor):** Bridge 99.9% USPS accuracy to {company} data standards [cite: 2026-03-23]. Practice [Specific Task].\\n\\n- **Day 7 (Simulation):** Final drill of the A3 team's mission [cite: 2026-03-28].",
      "strategic_priority": "The #1 thing they must prove in the interview."
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
