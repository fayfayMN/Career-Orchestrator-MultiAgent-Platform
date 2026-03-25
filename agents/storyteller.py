from openai import OpenAI

def draft_star_bullets(resume_text, gaps, jd, job_level, api_key):
    """
    Agent 3: The Storyteller (Problem-Solver Edition)
    Converts resume facts into high-stakes STAR stories.
    """
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    # SENIORITY-BASED STRATEGY
    if job_level == "Entry/Internship":
        focus = "Reliability, Accuracy, and Speed. Focus on fixing messy data and following processes."
    elif job_level == "Senior/Specialist":
        focus = "ROI, Architecture, and scaling systems to solve million-dollar problems."
    else:
        focus = "Independent delivery, specific tool mastery, and connecting data to business needs."

    prompt = f"""
    ACT AS: A Technical Storyteller for a {job_level} candidate.
    TASK: Turn these facts into 3 PUNCHY STAR stories.
    
    RESUME: {resume_text}
    JOB DESCRIPTION: {jd[:1000]}
    STRATEGY: {focus}
    GAPS TO BRIDGE: {gaps}

    STRICT RULES:
    1. NO FLUFF: Start with the problem, end with the number (%, $, or hours).
    2. THE MESS: Explicitly mention 'messy data' or 'unstructured records' if relevant.
    3. THE ACTION: Focus on what YOU built or fixed (Python, SQL, Automation).
    """

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You write technical stories that sound like a hard-working engineer."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
