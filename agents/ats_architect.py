# agents/ats_architect.py
import json
from openai import OpenAI

def run_ats_architect(resume_text, jd, job_level, company, gaps, api_key, writing_dna):
    """
    Dynamic Layer 2: The Impact-First Resume Rewriter.
    Tailors resume bullets to any level without hallucinating industry experience.
    """
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    prompt = f"""
    ACT AS: An expert Technical Resume Writer.
    MANDATE: STRICT NON-HALLUCINATION. Distinguish between 'Resume Bullets' and 'Interview Logic'.
    
    INSTRUCTIONS:
    1. DISCOVERY: Identify every distinct project/role in: {resume_text[:2000]}.
    2. THE PIVOT: Tailor technical methods (e.g., Python, SQL, Power BI) as 'Foundations' for {company}'s needs.
       - RULE: Do NOT claim the user has direct experience in {company}'s specific industry if it is not in the resume.
       - RULE: Frame existing technical tasks as 'directly applicable foundations' for {company}'s specific needs (e.g., Jira workflows or PIM audits).
    3. METRIC GROUNDING: 
       - Identify the candidate's highest quantitative metric or award (e.g., accuracy percentages, rankings, or tenure) [cite: 2026-03-23, 2026-01-09].
       - Keep these metrics as 'Proof of Operational Reliability' and 'Analytical Rigor' rather than falsely claiming they occurred in {company}'s domain.
    4. THE RESUME FORMULA (STRICT): 
       - Header: **Role/Project Title** | [Tools Used]
       - Bullet 1: [Action Verb] + [Technical Task] to solve [Business Problem].
       - Bullet 2: [Action Verb] + [Quantifiable Metric] (e.g., 99.9% accuracy or 70k rows) using [Tool]. [cite: 2026-03-23, 80, 83]
       - Bullet 3: [Action Verb] + [Business Impact] (e.g., reduced repeat work or improved data integrity). [cite: 58, 74, 84]
    5. NO LABELS: Do NOT use 'Problem:', 'Method:', or 'Result:' tags. Use professional, seamless sentences.

    OUTPUT FORMAT (STRICT JSON ONLY):
    {{
      "optimized_experience": [
        {{
          "Role": "Title",
          "Tech_Stack": "Tools",
          "Bullets": ["Bullet 1", "Bullet 2", "Bullet 3"]
        }}
      ],
      "recruiter_scan_verdict": "Blunt 1-sentence assessment of grit and fit.",
      "ats_keywords_hit": ["Keyword1", "Keyword2"]
    }}
    """
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            response_format={'type': 'json_object'}
        )
        content = response.choices[0].message.content.strip()
        
        # Mandatory: Strip Markdown backticks
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
            content = content.split("```")[0].strip()
            
        return json.loads(content)
    except Exception as e:
        return {
            "optimized_experience": [],
            "recruiter_scan_verdict": f"Error: {str(e)}",
            "ats_keywords_hit": []
        }
      
