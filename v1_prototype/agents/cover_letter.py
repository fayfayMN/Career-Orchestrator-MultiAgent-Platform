import json
from openai import OpenAI

def generate_cover_letter(resume, jd, company, job_level, api_key, style_sample=""):
    """
    Agent 8: The Dynamic Cover Letter Composer.
    Implements the OpenAI 4-paragraph structure with zero hardcoding.
    """
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    # AI-Slop Filter: Professional but blunt
    blacklist = ["synergy", "spearheaded", "passionate", "leverage", "vibrant", "dynamic", "medication", "pharma"]

    prompt = f"""
    ACT AS: A Technical Career Narrative Architect.
    Linguistic DNA Template: {style_sample[:1000] if style_sample else "Professional & Blunt"}

    STRICT RULES:
    1. INDUSTRY GROUNDING: Analyze this JD: {jd[:1500]}. ONLY use vocabulary and themes found there.
    2. LEVEL-GATE: This is an {job_level} role. 
       - If 'Intern/Junior': Focus on GPA, learning speed, and 'Eagerness to contribute'.
       - If 'Senior/Lead': Focus on ROI, system architecture, and leadership.
    3. THE STAR BRIDGE: Search {resume[:2000]} for the candidate's highest quantitative metric (e.g., %, $, #, or ranking).
       - PIVOT that specific win to solve a core problem in the {company} JD.

    TASK: Write a 4-paragraph letter following this structure:
    - Para 1 (The Hook): Level-appropriate intro mentioning the {job_level} role and your #1 technical win.
    - Para 2 (The Technical Fit): Match technical skills from resume to JD requirements using STAR-inspired examples.
    - Para 3 (The Operational Discipline): Explain how your unique path/metrics prepare you for {company}'s "blind spots."
    - Para 4 (The Mission): Show alignment with {company}'s specific mission (e.g., assembling TVs for Element). [cite: 56, 85]

    VETO: Strictly avoid these AI-slop words: {', '.join(blacklist)}.
    
    OUTPUT FORMAT (STRICT JSON ONLY):
    {{
      "cover_letter_narrative": "Subject: {job_level} Application - {company}\\n\\nDear Hiring Manager,\\n\\n[Paragraphs]...\\n\\nSincerely,\\n\\n[Name]",
      "value_anchor": "The specific bridge between candidate grit and {company}."
    }}
    """

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "system", "content": "You are a professional business writer who hates fluff."},
                      {"role": "user", "content": prompt}],
            response_format={'type': 'json_object'}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"cover_letter_narrative": f"Error: {str(e)}", "value_anchor": "N/A"}
