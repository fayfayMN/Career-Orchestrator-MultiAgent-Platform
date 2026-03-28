# agents/strategy_arch.py
import json
from openai import OpenAI
    
def run_strategy_architect(resume_text, jd, job_level, company, api_key, strengths, weaknesses, writing_dna):
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    
    prompt = f"""
    ACT AS: A Senior Technical Career Strategist.
    MANDATE: Perform a 'Differential Gap Analysis' between Resume and JD.
    
    INPUT DATA:
    - Resume: {resume_text[:2000]}
    - Target JD: {jd}
    - User Context: Strengths({strengths}), Weaknesses({weaknesses})
    - Target: {company} ({job_level} role)

    TASK:
    # Inside the prompt:
    "1. GAP IDENTIFICATION: Compare Resume to {jd}. Identify 3 'High-Risk' gaps, specifically looking for industry compliance (e.g., HIPAA, 21 CFR Part 11) or advanced tool requirements (e.g., ETL pipelines, Warehousing)."
    2. RESOURCE MAPPING: For each gap, provide a specific, high-depth learning link (e.g., GitHub Zoomcamps, Documentation, or SQLZoo). [cite: 46]
    3. PROJECT PIVOT: Identify the user's strongest existing project and re-architect it as a solution for {company}. 
    4. GRIT BRIDGE: Find the highest 'Accuracy' or 'Tenure' metric in the resume. Bridge it to {company}'s operational standards.

    OUTPUT FORMAT (STRICT JSON ONLY):
    {{
      "match_score": 0-100,
      "persona_assessment": "Blunt assessment of their grit.",
      "missing_gaps": ["Gap 1", "Gap 2", "Gap 3"],
      "learning_syllabus": "## 📅 Strategic 7-Day Sprint\\n\\n- **Day 1-2 (Technical Foundation):** Master [Gap Name]. **Resource:** [Clickable Markdown Link].\\n\\n- **Day 3-4 (The Build):** Project: '[Title]'. Task: Pivot [User's Best Project] to solve [{company} Problem].\\n\\n- **Day 5-6 (Operational Rigor):** Bridge [User Metric] to [{company} Standard].\\n\\n- **Day 7 (Simulation):** Final drill of the [{company}] mission [cite: 2026-03-28].",
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
        # Sanitize Markdown if AI ignores response_format
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        return json.loads(content)
    except Exception as e:
        return {"error": str(e), "match_score": 0, "learning_syllabus": "Technical Failure"}
    


   
   
