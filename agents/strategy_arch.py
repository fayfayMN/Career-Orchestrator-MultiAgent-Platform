import json
from openai import OpenAI

def run_strategy_architect(resume, jd, job_level, company_name, api_key, user_strengths, user_weaknesses, writing_dna):
    """
    Agent 1 & 2 Hybrid: The Auditor + Tutor
    Goal: High speed without losing V1 tactical depth.
    """
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    
    prompt = f"""
    ACT AS: Senior Recruiter & Practical Technical Mentor at {company_name}.
    
    USER CONTEXT:
    - Target: {company_name} | Level: {job_level} | Style: {writing_dna}
    - Persona: Strengths({user_strengths}), Gaps({user_weaknesses})
    
    RESUME: {resume}
    JOB DESCRIPTION: {jd}
    
    TASK: Provide a surgical gap analysis AND a V1-style learning roadmap.
    
    OUTPUT FORMAT (STRICT JSON ONLY):
    {{
      "match_score": 85,
      "persona_assessment": "Blunt summary of fit and grit",
      "missing_gaps": ["skill1", "skill2"],
      "learning_syllabus": "## 🛠️ 48-Hour Technical Sprint\\n### [Skill Name]\\n- **Fundamental:** 2-sentence blunt explanation\\n- **Resource:** Exact YouTube search terms\\n- **Mini-Project:** 2-hour hands-on task\\n- **Interview Script:** 'When they ask, I say...'\\n\\n## 🚀 Quva-Specific Application\\n- [Specific healthcare data utility]"
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
