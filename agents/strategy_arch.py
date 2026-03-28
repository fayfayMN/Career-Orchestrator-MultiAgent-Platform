# agents/strategy_arch.py
import json
from openai import OpenAI
    
def run_strategy_architect(resume_text, jd, job_level, company, api_key, strengths, weaknesses, writing_dna):
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    
    prompt = f"""
    ACT AS: A Technical Mentor & Career Strategist.
    MANDATE: STRICT NON-HALLUCINATION. Distinguish between 'Current Skills' and 'Learning Goals'.
    Perform a 'Differential Gap Analysis' between Resume and JD.
    
    INPUT:
    - Resume: {resume_text[:2000]}
    - Target: {company} ({job_level} role)
    - JD: {jd[:1500]}
    - User Context: Strengths({strengths}), Weaknesses({weaknesses})
    
    TASK: Create a 7-Day 'Actionable Workbook' Syllabus or Sprint for the {job_level} role at {company}.
    
    DYNAMIC RULES:
    1. THE GAP: Identify specific technical gaps (e.g., PIM, Jira, or SQL) without assuming prior knowledge.
    2. THE RESOURCE: Provide real links to documentation (e.g., 'Pimcore Docs') instead of pretending they know the tool.
    3. THE PROJECT: Frame tasks as 'Skill Transfer Labs'. 
       - Task: Apply logic from a known project (e.g., your 70k survey) to a sample dataset relevant to {company}. 
    4. NO LIES: Do NOT suggest the user has built systems (like image pipelines) not found in their resume.

    STYLE REQUIREMENTS (STRICT):
    For every technical gap identified, use this exact structure:
    ### **[Skill Name]**
    **THE FUNDAMENTAL:** [1-sentence core concept to master]
    **THE RESOURCE:** [Specific Clickable Markdown Link to Official Docs or GitHub]
    **THE MINI-PROJECT:** [A 2-hour task to prove the skill using their resume data]
    **INTERVIEW TALKING POINT:** [A STAR-based script bridging their grit to this new skill]

    DAY-BY-DAY STRUCTURE:
    - Day 1-2: Core Technical Gaps.
    - Day 3-4: The Build. Project: 'Pivot [User's Best Project] into a {company} Solution'.
    - Day 5-6: Operational Rigor. Bridge their highest metric (e.g., 99.9% USPS accuracy) to {company} standards.
    - Day 7: Final Simulation & Mission Drill.

    OUTPUT FORMAT (STRICT JSON):
    {{
      "match_score": 0-100,
      "persona_assessment": "Blunt assessment of grit.",
      "missing_gaps": ["Gap 1", "Gap 2", "Gap 3"],
      "learning_syllabus": "[INSERT FULL MARKDOWN SYLLABUS HERE]",
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
        
        # Sanitize Markdown if AI ignores response_format
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        return json.loads(content)
    except Exception as e:
        return {"error": str(e), "match_score": 0, "learning_syllabus": "Technical Failure"}
