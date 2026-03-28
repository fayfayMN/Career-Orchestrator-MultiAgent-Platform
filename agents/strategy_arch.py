import json
from openai import OpenAI

# agents/strategy_arch.py
import json
from openai import OpenAI

def run_strategy_architect(resume_text, jd, job_level, company, api_key, strengths, weaknesses, writing_dna):
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    
    prompt = f"""
    ACT AS: A Technical Strategy Lead.
    TASK: Generate a 1-week preparation roadmap for {company}.
    
    INPUTS:
    - Resume: {resume_text[:1500]}
    - Gaps identified by user: {weaknesses}
    
    MANDATE: 
    - Provide a specific 7-day syllabus.
    - Include 1 'Proof-of-Concept' project to close a gap.
    - Provide resource types (e.g., 'Documentation for AWS S3' or 'LeetCode SQL').

    OUTPUT FORMAT (STRICT JSON):
    {{
      "match_score": 85,
      "persona_assessment": "Grizzled Data Realist with 99.9% USPS accuracy [cite: 2026-03-23].",
      "missing_gaps": ["List 2-3 specific technical gaps"],
      "learning_syllabus": "## 📅 V1 Strategic 7-Day Sprint\\n
      - **Day 1-2 (Technical Gaps):** Focus on [Gap 1]. Resource: [Specific Resource].\\n
      - **Day 3-4 (The Project):** Build a [Mini-Project Name] to demonstrate [Skill].\\n
      - **Day 5-6 (Compliance/Integrity):** Review HIPAA and Pharmaceutical Data Integrity for {company} [cite: 2026-03-28].\\n
      - **Day 7 (Simulation):** Final drill focusing on the A3 Team's mission.",
      "strategic_priority": "Bridge the gap between academic theory and operational reliability."
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
