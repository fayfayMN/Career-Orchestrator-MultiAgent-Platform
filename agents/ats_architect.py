# agents/ats_architect.py
import json
import re
from openai import OpenAI

def run_ats_architect(resume_text, jd, job_level, company, gaps, api_key, writing_dna):
    """
    Dynamic Layer 2: The Impact-First Resume Rewriter.
    Strictly converts STAR logic into professional resume bullets.
    """
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    # The prompt now uses 'Negative Constraints' to explicitly ban labels like 'Problem:'
    prompt = f"""
    ACT AS: A Senior Technical Resume Architect for {company}.
    MANDATE: STRICT NON-HALLUCINATION. Distinguish between 'Resume Bullets' and 'Interview Logic'.
    
    INPUT DATA:
    - Master Resume: {resume_text[:3000]}
    - Target JD: {jd[:1000]}
    - Candidate Strengths: High-Grit, Analytical Rigor, Operational Excellence [cite: 2026-03-23, 2026-03-26].

    INSTRUCTIONS:
    1. DISCOVERY: Extract every project/role. Pivot technical foundations (Python, SQL, Power BI) to {company}'s needs.
    2. THE RESUME FORMULA (STRICT): 
       - Header: **Role/Project Title** | [Tools Used]
       - Bullet 1 (Action): [Action Verb] + [Technical Task] to solve [Business Problem].
       - Bullet 2 (Metric): [Action Verb] + [Quantifiable Metric] (e.g., 99.9% accuracy or 70k rows) using [Specific Tool].
       - Bullet 3 (Impact): [Action Verb] + [Business ROI] (e.g., automated reporting or improved data integrity).

    3. THE 'LABEL BAN' (CRITICAL): 
       - DO NOT use tags like 'Problem:', 'Method:', 'Result:', or 'STAR:'.
       - DO NOT use icons like '✅' or '•' inside the JSON strings.
       - Every bullet must be a clean, standalone professional sentence starting with a strong Action Verb.

    4. INDUSTRY FENCE: Frame the candidate's wins (e.g., #1 state ranking or USPS accuracy) as 'Foundational Logic' for {company}. [cite: 2026-01-09, 2026-03-23]

    OUTPUT FORMAT (STRICT JSON ONLY):
    {{
      "optimized_experience": [
        {{
          "Role": "Professional Title",
          "Tech_Stack": "Python, SQL, etc.",
          "Bullets": ["Bullet 1", "Bullet 2", "Bullet 3"]
        }}
      ],
      "recruiter_scan_verdict": "Blunt 1-sentence assessment of fit.",
      "ats_keywords_hit": ["Keyword1", "Keyword2"]
    }}
    """

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            response_format={'type': 'json_object'},
            temperature=0.3 # Lower temperature ensures more consistent formatting
        )
        
        content = response.choices[0].message.content.strip()
        
        # --- ROBUST JSON CLEANING ---
        # Removes Markdown code blocks if the model ignores the response_format instruction
        content = re.sub(r'```json\s*|```\s*', '', content) 
        
        data = json.loads(content)

        # --- POST-PROCESSING: LABEL PURGE ---
        # Extra safety layer to remove any labels the LLM leaked into the bullets
        labels_to_strip = ["Problem:", "Method:", "Result:", "Technical Method:", "Business Impact:", "STAR:"]
        for item in data.get("optimized_experience", []):
            clean_bullets = []
            for bullet in item.get("Bullets", []):
                for label in labels_to_strip:
                    bullet = bullet.replace(label, "").strip()
                clean_bullets.append(bullet)
            item["Bullets"] = clean_bullets

        return data

    except Exception as e:
        return {
            "optimized_experience": [
                {
                    "Role": "Architectural Error",
                    "Tech_Stack": "N/A",
                    "Bullets": [f"System failed to parse resume: {str(e)}"]
                }
            ],
            "recruiter_scan_verdict": "Pipeline fracture detected.",
            "ats_keywords_hit": []
        }
