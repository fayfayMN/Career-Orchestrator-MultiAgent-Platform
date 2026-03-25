from openai import OpenAI

def draft_star_bullets(resume_text, gaps, jd, job_level, api_key):
    """
    Agent 3: The Storyteller (ATS-Bullet Edition)
    Converts resume facts into high-impact, professional resume bullets.
    """
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    prompt = f"""
    ACT AS: A Senior Technical Recruiter and ATS Optimization Expert.
    TASK: Convert the candidate's Resume facts into 3 PROFESSIONAL RESUME BULLETS.
    
    RESUME: {resume_text}
    JOB DESCRIPTION: {jd[:1000]}
    JOB LEVEL: {job_level}

    STRICT RESUME RULES:
    1. NO PERSONAL PRONOUNS: Never use 'I', 'me', or 'my'.
    2. ACTION VERBS: Start every bullet with a strong verb (e.g., Engineered, Optimized, Automated).
    3. ATS KEYWORDS: Naturally include keywords from the JD (e.g., SQL, Python, Documentation, Process Improvement).
    4. FORMAT: [Action Verb] + [Specific Task/Tool] + [Quantifiable Result].
    5. NO CONVERSATIONAL FILLER: No "Here is what I did" or "I am a worker." Just the bullets.
    """

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are an ATS-expert. You only output professional, third-person resume bullets."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
