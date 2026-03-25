from openai import OpenAI

def judge_persona_fit(traits, weakness, style, jd, api_key):
    """
    Agent 3.5: The Persona Judge
    Analyzes culture fit before the writing begins.
    """
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    
    prompt = f"""
    Compare this PERSONA to this JOB DESCRIPTION.
    STRENGTHS: {traits} | WEAKNESS: {weakness} | STYLE: {style}
    JOB: {jd[:1000]} 

    TASK: Give a 2-sentence blunt assessment: 
    1. Does their style match the job culture?
    2. How can they leverage their 'weakness' as a strength in this role?
    """
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def refine_to_human_voice(draft_text, traits, user_writing_sample, job_level, api_key):
    """
    Agent 4: The Voice Filter (Jargon-Blacklist Edition)
    Rewrites AI-slop into 'Blue-Collar' professional grit.
    """
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    # SENIORITY STRATEGY
    if job_level == "Entry/Internship":
        strategy = "Focus on: Cleaning data, fixing broken spreadsheets, and being a reliable workhorse."
    elif job_level == "Senior/Specialist":
        strategy = "Focus on: ROI, solving systemic business leaks, and scaling output."
    else:
        strategy = "Focus on: Independent project delivery and technical tool mastery."

    # THE JARGON BLACKLIST
    blacklist = [
        "integrity", "rigor", "equipped", "initiatives", "structuring chaos", 
        "multifaceted", "synergy", "tapestry", "meticulous", "spearheaded", 
        "passionate", "leverage", "foster", "delivering excellence", "deep-dive"
    ]

    style_guide = f"""
    ACT AS: A blunt, practical career coach for a candidate with these traits: {traits}.
    STRATEGY: {strategy}
    WRITING DNA: {user_writing_sample}
    
    CRITICAL RULES (NO AI-SLOP):
    1. BLACKLIST: Never use these words: {', '.join(blacklist)}.
    2. BLUE-COLLAR VERBS: Use verbs like: 'built', 'fixed', 'cleaned', 'ran', 'saved', 'organized'.
    3. NO METAPHORS: Do not say 'bridge the gap' or 'structure chaos'. Say 'fix the error' or 'clean the messy data'.
    4. PUNCHY SENTENCES: If a sentence is longer than 20 words, cut it in half.
    """

    prompt = f"{style_guide}\n\nTASK: Rewrite these STAR bullets into a human-grit cover letter/narrative:\n{draft_text}"

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a blunt coach who hates corporate jargon. Speak like a person who does the work, not a person who writes the brochures."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
