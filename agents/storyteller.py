from openai import OpenAI

def draft_star_bullets(resume_text, gaps, jd, job_level, api_key):
    """
    Agent 3: The Storyteller
    Generates raw STAR bullets tailored to the target seniority level.
    """
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    # SENIORITY-BASED ANGLE
    if job_level == "Entry/Internship":
        focus_prompt = """
        FOCUS: Operational Utility & Technical Support.
        Highlight: Accuracy, ability to follow complex documentation, Excel/Python automation for 'messy' data, 
        and high-speed task completion (USPS background). 
        Avoid: High-level strategy or 'leading' teams.
        """
    elif job_level == "Senior/Specialist":
        focus_prompt = """
        FOCUS: Architecture & Institutional Impact.
        Highlight: End-to-end pipeline design, ROI, leading technical initiatives, 
        and solving systemic business problems with AI.
        """
    else:
        focus_prompt = """
        FOCUS: Independent Problem Solving.
        Highlight: Specific project delivery, tool mastery (SQL/Deep Learning), 
        and bridging the gap between data and insights.
        """

    prompt = f"""
    ROLE: Expert Career Storyteller.
    TASK: Convert the candidate's Resume into 3 high-impact STAR bullets for this Job.
    
    RESUME: {resume_text}
    JOB DESCRIPTION: {jd[:1000]}
    STRATEGY: {focus_prompt}
    GAPS TO BRIDGE: {gaps}

    FORMAT:
    - Situation: The context.
    - Task: The challenge.
    - Action: THE CORE (Focus on {job_level} appropriate actions).
    - Result: Quantifiable outcome (%, $, or hours saved).
    """

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a technical storyteller who specializes in STAR format."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
