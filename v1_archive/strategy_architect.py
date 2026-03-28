from openai import OpenAI
import json

def run_strategy_architect(resume, jd, job_level, company_name, api_key):
    """
    Consolidated Layer 1: Auditor + Tutor
    Goal: Identify gaps and build a roadmap in one reasoning cycle.
    """
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    prompt = f"""
    ACT AS: A Senior Technical Recruiter and Career Coach.
    CONTEXT: The candidate is applying to {company_name} for a {job_level} role.
    
    MASTER RESUME: {resume}
    JOB DESCRIPTION: {jd}

    TASK:
    1. AUDIT: Compare the resume against the JD. Assign a Match Score (0-100).
    2. GAP ANALYSIS: Identify the top 3 missing technical or soft skills.
    3. SYLLABUS: Create a 48-hour "Sprint" to bridge those specific gaps.
    
    OUTPUT FORMAT (STRICT JSON):
    {{
      "match_score": int,
      "audit_summary": "string",
      "missing_gaps": ["list of strings"],
      "learning_syllabus": "markdown_formatted_string"
    }}
    """

    try:
        response = client.chat.completions.create(
            model="deepseek-chat", # Tier 1 model for Logic
            messages=[{"role": "system", "content": "You are a strategic career architect."},
                      {"role": "user", "content": prompt}],
            response_format={'type': 'json_object'}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {{"error": str(e)}}
