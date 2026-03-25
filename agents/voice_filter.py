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
    Agent 4: The Voice Filter
    Adjusts the seniority and tone based on the target job level.
    """
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    # STRATEGY SELECTION LOGIC
    if job_level == "Entry/Internship":
        strategy = """
        TONE: The 'Hungry Automator.' 
        Focus on: High-speed execution, documentation, reliability, and technical utility. 
        DE-ENGINEER: Change high-level jargon (e.g., 'Architected Frameworks') to operational value (e.g., 'Streamlined Data Workflows'). 
        Frame yourself as the person who can make the team's boring tasks disappear using advanced tools.
        """
    elif job_level == "Senior/Specialist":
        strategy = """
        TONE: The 'Strategic Architect.' 
        Focus on: ROI, leadership, scaling systems, and cross-functional impact. 
        Use high-level technical terms. Frame work as 'Institutional Improvement.'
        """
    else: # Associate/Professional
        strategy = """
        TONE: The 'Problem Solver.' 
        Focus on: Independent project delivery, specific technical mastery (SQL/Python), and accuracy.
        """

    style_guide = f"""
    ACT AS: A career coach refining a candidate's voice.
    STRATEGY: {strategy}
    USER TRAITS: {traits}
    WRITING DNA: {user_writing_sample}
    
    CONSTRAINTS:
    1. NO AI-SLOP: Strictly delete 'meticulous,' 'tapestry,' 'spearheaded,' or 'passionate.'
    2. STAR FORMAT: Ensure every bullet point leads to a concrete, quantifiable result.
    3. AUTHENTICITY: Weave in their 'Writing DNA' to keep the tone human.
    """

    prompt = f"{style_guide}\n\nTASK: Rewrite these STAR bullets for a {job_level} role:\n{draft_text}"

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a blunt, practical career coach adjusting seniority levels."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
