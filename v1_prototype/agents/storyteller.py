from openai import OpenAI

def draft_star_bullets(resume_text, gaps, jd, job_level, api_key):
    """
    Agent 3: The Storyteller (ATS-Bullet Edition)
    Converts raw experience into structured, professional resume bullets.
    """
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    prompt = f"""
    ACT AS: A Senior Technical Recruiter.
    TASK: Convert the candidate's Resume facts into 3-4 PROFESSIONAL RESUME BULLETS for a {job_level} role.
    
    RESUME: {resume_text}
    JOB DESCRIPTION: {jd[:1000]}

    STRICT RESUME RULES:
    1. FORMAT: Use a bold Header for the Project/Role, then 3-4 bullet points.
    2. BULLET STRUCTURE: Start with a strong Action Verb (Engineered, Led, Designed, Delivered).
    3. NO PERSONAL PRONOUNS: Never use 'I', 'me', 'my', or 'we'.
    4. TECH STACK: Explicitly mention Python, SQL, Power BI, etc., within the bullets.
    5. DATA-DRIVEN: Mention the 70,000 records, the 1st place rank, and the 99.9% accuracy.
    """

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You output only clean, professional resume bullets. No conversational filler."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
