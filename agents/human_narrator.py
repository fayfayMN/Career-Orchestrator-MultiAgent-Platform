import json
from openai import OpenAI

def run_human_narrator(resume_text, jd, persona, writing_dna, company, job_level, api_key, style_sample=""):
    """
    Dynamic Narrative Architect: Tailors the "OpenAI Standard" to any level.
    """
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    
    # AI-Slop Filter: Removes 'Passionate' and 'Synergy'
    blacklist = ["synergy", "spearheaded", "passionate", "leverage", "vibrant", "dynamic", "medication", "pharma"]

    prompt = f"""
    ACT AS: A Technical Career Narrative Architect.
    STRICT RULE: Analyze this JD: {jd[:1500]}. ONLY use industry themes found there.
    Linguistic DNA: {style_sample[:1000] if style_sample else writing_dna}
    
    TASK: Write a 3-paragraph Cover Letter for a {job_level} role at {company}.
    
    DYNAMIC LOGIC:
    1. THE HOOK ({job_level}): 
       - If 'Intern/Junior': Focus on GPA, competition wins, and 'Eagerness to contribute' to {company}'s specific tech stack.
       - If 'Senior/Lead': Focus on ROI, team leadership, and architectural vision.
    2. THE STAR BRIDGE: Identify the user's #1 metric (e.g., 99.9% accuracy or #1 ranking). [cite: 127, 102]
       - PIVOT that metric to {company}'s "Key Responsibilities" (e.g., Jira normalization or SLA tracking). [cite: 87]
    3. THE ALIGNMENT: Reference {company}'s mission (e.g., 'assembling TVs in the USA' for Element). [cite: 85]

    VETO: Strictly avoid {', '.join(blacklist)}.
    
    OUTPUT FORMAT (STRICT JSON ONLY):
    {{
      "cover_letter_narrative": "Subject: {job_level} Application - {company}\\n\\nDear Hiring Manager,\\n\\n[Para 1: Level-Appropriate Hook]\\n\\n[Para 2: STAR-based Pivot using Metrics]\\n\\n[Para 3: Mission Alignment]\\n\\nSincerely,\\n\\n[Name]",
      "value_anchor": "Briefly state the specific bridge between the candidate and {company}."
    }}
    """

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "system", "content": "You are a blunt career coach. No fluff."},
                      {"role": "user", "content": prompt}],
            response_format={'type': 'json_object'}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}
