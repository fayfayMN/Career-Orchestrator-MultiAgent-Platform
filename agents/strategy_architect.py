import json
from openai import OpenAI

def run_strategy_architect(resume, jd, job_level, company_name, api_key):
    """
    Consolidated Layer 1: Auditor + Tutor.
    Identifies the 'Value Anchor' and technical gaps in one reasoning cycle.
    """
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    prompt = f"""
    ACT AS: A Senior Technical Recruiter and Career Coach.
    CONTEXT: The candidate is applying to {company_name} for a {job_level} role.
    
    MASTER RESUME: {resume}
    JOB DESCRIPTION: {jd}

    TASK:
    1. AUDIT: Compare the resume against the JD. Assign a Match Score (0-100).
    2. GAP ANALYSIS: Identify the top 3-5 missing technical or soft skills required by the JD.
    3. SYLLABUS: Create a 48-hour "Hungry Automator" Sprint to bridge those specific gaps.
    4. AUDIT SUMMARY: Write a 2-sentence summary of the candidate's 'Unique Grit' (e.g., USPS experience + 3.9 GPA).

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
            model="deepseek-chat", # Tier 1 Logic Model
            messages=[
                {"role": "system", "content": "You are a strategic career architect who values blunt truth over fluff."},
                {"role": "user", "content": prompt}
            ],
            response_format={'type': 'json_object'}
        )
        # Parse the JSON string from the model's message content
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        # Return a structured error so app.py doesn't crash
        return {
            "match_score": 0,
            "audit_summary": f"Error: {str(e)}",
            "missing_gaps": [],
            "learning_syllabus": "Check API connection."
        }
