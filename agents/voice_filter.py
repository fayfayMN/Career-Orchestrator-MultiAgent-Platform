from openai import OpenAI

def judge_persona_fit(traits, weakness, style, jd, api_key):
    """
    Agent 3.5: The Persona Judge
    """
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    prompt = f"Traits: {traits} | Weakness: {weakness} | Style: {style} | Job: {jd[:800]}\nAssessment:"
    response = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content

def refine_to_human_voice(draft_text, traits, user_writing_sample, job_level, api_key):
    """
    Agent 4: The Voice Filter (Human-Grit Edition)
    Strips 'Professional Ego' and replaces it with 'Workhorse Reality.'
    """
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    # JARGON BLACKLIST (The AI-Slop Killer)
    blacklist = [
        "integrity", "rigor", "equipped", "initiatives", "structuring chaos", 
        "multifaceted", "synergy", "tapestry", "meticulous", "spearheaded", 
        "passionate", "leverage", "foster", "delivering excellence", "deep-dive",
        "analytical asset", "substantive", "precisely suited", "passionate"
    ]

    style_guide = f"""
    ACT AS: A blunt, hard-working Data Science student (3.9 GPA) who used to be a USPS City Carrier.
    STRATEGY: You are a 'Hungry Automator.' You write like a person who fixes things, not someone who writes brochures.
    WRITING DNA: {user_writing_sample}
    
    HUMAN-VOICE CONSTRAINTS:
    1. USE CONTRACTIONS: Use 'I'm', 'don't', 'can't', 'I've'.
    2. THE 'MESS' RULE: Use 'messy data' instead of 'unstructured assets.'
    3. NO 'EXPRESSING INTEREST': Get straight to the facts: 3.9 GPA, 1st place AI win, USPS grit.
    4. BLACKLIST: Never use: {', '.join(blacklist)}.
    5. PUNCHY: Keep sentences short. If it sounds like a textbook, delete it.
    """

    prompt = f"{style_guide}\n\nTASK: Rewrite this into a human-grit cover letter/narrative:\n{draft_text}"

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You hate 'corporate speak'. Speak like a person who does the work."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
