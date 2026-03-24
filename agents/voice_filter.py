from openai import OpenAI

def judge_persona_fit(traits, weakness, style, jd, api_key):
    """
    Agent 3.5: The Persona Judge
    Analyzes if the user's personality matches the job culture.
    """
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    
    prompt = f"""
    Compare this PERSONA to this JOB DESCRIPTION.
    STRENGTHS: {traits}
    WEAKNESS: {weakness}
    STYLE: {style}
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

def refine_to_human_voice(draft_text, traits, user_writing_sample, api_key):
    """
    Agent 4: The Voice Filter
    Rewrites AI-slop into the user's authentic professional voice.
    """
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    style_guide = f"""
    ACT AS: A career coach for a candidate with these traits: {traits}.
    WRITING DNA TO MATCH: {user_writing_sample}
    
    CONSTRAINTS:
    1. NO AI-SLOP: Remove 'meticulous,' 'tapestry,' 'spearheaded,' or 'passionate.'
    2. PUNCHY: Use direct, short sentences.
    3. REAL IMPACT: Link every skill to a practical result (e.g., 'saved 10 hours of manual data entry').
    """

    prompt = f"{style_guide}\n\nTASK: Rewrite these STAR bullets to match this voice:\n{draft_text}"

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a blunt, practical career coach."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
