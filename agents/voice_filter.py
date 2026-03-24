from openai import OpenAI

def refine_to_human_voice(draft_text, user_traits, user_writing_sample, api_key):
    """
    Agent 4: The Voice Filter
    Now handles ANY user by combining their traits and writing DNA.
    """
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    # This is the "Universal Engine" Prompt
    dynamic_style_guide = f"""
    ROLE: Professional Human Persona Architect.
    
    INPUT DATA:
    - User Personality/Strengths: {user_traits}
    - User Writing DNA Sample: {user_writing_sample}
    
    CONSTRAINTS:
    1. DELETE AI-SLOP: Strictly remove 'meticulous,' 'passionate,' 'tapestry,' or 'spearheaded.'
    2. MATCH TONE: If the sample is blunt, stay blunt. If it's warm, stay warm.
    3. PRACTICAL IMPACT: Link every technical skill to a human result.
    4. AUTHENTICITY: Use the 'User Personality' to add grit and real-world flavor.
    """

    prompt = f"{dynamic_style_guide}\n\nTASK: Rewrite these STAR bullets to match THIS candidate's voice:\n{draft_text}"

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a blunt, practical career coach refining a student's authentic persona."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
