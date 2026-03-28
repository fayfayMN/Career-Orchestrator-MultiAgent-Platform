from openai import OpenAI

def generate_targeted_resume(master_resume, jd, job_level, api_key):
    """
    Agent 7: The ATS Architect
    Rebuilds the resume structure to match the JD's keyword frequency.
    """
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    prompt = f"""
    ACT AS: An ATS Optimization Expert.
    TASK: Rewrite the Master Resume to perfectly align with this JD.
    
    MASTER RESUME: {master_resume}
    JOB DESCRIPTION: {jd[:1000]}
    LEVEL: {job_level}

    INSTRUCTIONS:
    1. KEYWORD INJECTION: Identify the top 5 technical and 5 soft skills in the JD. Ensure they appear in the 'Skills' and 'Experience' sections.
    2. RE-TITLE EXPERIENCE: If the JD asks for 'Process Improvement' and the candidate did that at USPS (logistics optimization), explicitly use that term.
    3. QUANTIFIABLE IMPACT: Keep the 99.9% accuracy and 70k records.
    4. FORMAT: 
       - Summary (2 sentences, high-impact)
       - Technical Skills (Categorized)
       - Experience (ATS-optimized bullets)
       - Education
    """

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are an expert at bypassing ATS filters while maintaining professional integrity."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
