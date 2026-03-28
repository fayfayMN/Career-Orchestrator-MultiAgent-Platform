import json
from openai import OpenAI

# agents/strategy_arch.py
import json
from openai import OpenAI

def run_strategy_architect(resume_text, jd, job_level, company, api_key, strengths, weaknesses, writing_dna):
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    
    prompt = f"""
    ACT AS: A Senior Technical Career Strategist.
    MANDATE: Perform a Gap-to-Resource Mapping for any candidate.
    
    INPUT:
    - Resume: {resume_text[:2000]}
    - Target JD: {jd}
    - Strengths/Weaknesses: {strengths} / {weaknesses}
    - Target: {company} ({job_level} role)

    TASK:
    1. ANALYZE GAPS: Compare Resume skills against {jd}. Identify all the "Hard Gaps" (e.g., ETL, Cloud, HIPAA).
    2. DISCOVER GRIT: Identify the candidate's highest-metric achievement (e.g., 99.9% accuracy, #1 ranking, or 7-year tenure) [cite: 2026-03-23, 2026-01-09].
    3. BUILD SYLLABUS: Create a 7-Day Sprint.
       - Day 1-2 (Gaps): Suggest 1 specific, free, high-speed resource for each Gap (e.g., 'SQLZoo', 'Microsoft Learn', or 'Metropolitan State Library').
       - Day 3-4 (Build): Design a 'Proof-of-Concept' project that migrates their best resume project into a solution for {company}.
       - Day 5-6 (Rigor): Explicitly bridge their 'Grit' achievement to {company}'s operational standards.

    OUTPUT FORMAT (STRICT JSON ONLY):
    {{
      "match_score": 0-100,
      "persona_assessment": "Short Blunt assessment of their grit.",
      "missing_gaps": ["List specific technical gaps"],
      "learning_syllabus": "## 📅 Strategic 7-Day Sprint\\n\\n- **Day 1-2 (Technical Foundation):** Master [Gaps]. **Resource:** [Specific Link/Tool].\\n\\n- **Day 3-4 (The Build):** Project: '[Title]'. Task: Pivot [User Project] to solve [{company} Problem].\\n\\n- **Day 5-6 (Operational Rigor):** Bridge [User Metric] to [{company} Standard].\\n\\n- **Day 7 (Simulation):** Final drill of the [{company}] mission [cite: 2026-03-28].",
      "strategic_priority": "The #1 thing to prove in the interview."
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
