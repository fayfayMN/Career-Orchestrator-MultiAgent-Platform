from openai import OpenAI
import json

def run_ats_architect(resume, gaps, jd, job_level, api_key):
    """
    Consolidated Layer 2: Storyteller + Resume Pro
    Goal: Rebuild the resume structure and draft STAR bullets in one pass.
    """
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    prompt = f"""
    ACT AS: An ATS Optimization Expert and Technical Resume Writer.
    CONTEXT: Candidate is a 3.9 GPA Data Science student[cite: 45].
    TARGET: AI Software Engineering Intern @ Life Time[cite: 17].
    
    MASTER RESUME: {resume}
    GAPS IDENTIFIED: {gaps}
    JOB DESCRIPTION: {jd}

    TASK:
    1. KEYWORD INJECTION: Map {jd} keywords (e.g., APIs, Python, Java, Cloud) to existing experience[cite: 17].
    2. RE-ARCHITECT: Group skills into "Core Technical" and "Engineering Tools"[cite: 42].
    3. STAR BULLETS: Rewrite experience (USPS, Projects) into 3-4 high-impact bullets using action verbs[cite: 49, 72].
    
    OUTPUT FORMAT (STRICT JSON):
    {{
      "targeted_summary": "string",
      "optimized_skills_section": {{ "Category": ["Skill1", "Skill2"] }},
      "ats_experience_bullets": [
          {{ "Company": "string", "Bullets": ["List of STAR bullets"] }}
      ]
    }}
    """

    try:
        response = client.chat.completions.create(
            model="deepseek-chat", # Tier 1 for precision
            messages=[{"role": "system", "content": "You are an expert ATS Architect."},
                      {"role": "user", "content": prompt}],
            response_format={'type': 'json_object'}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}
