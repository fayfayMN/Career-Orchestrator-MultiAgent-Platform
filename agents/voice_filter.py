# agents/voice_filter.py
from openai import OpenAI

def refine_to_human_voice(draft_text, api_key):
    """
    Agent 4: The Voice Filter
    Applies the 'Resilience & Data' style guide extracted from Feifei's personal statement.
    """
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    # This is the "Feifei Persona" Prompt
    style_guide = """
    ACT AS: Feifei Li, a resilient Data Science student (3.9 GPA) and TRIO scholar.
    
    STYLE CONSTRAINTS:
    1. NO FLUFF: Remove AI words like 'meticulous,' 'passionate,' 'tapestry,' or 'spearheaded.'
    2. THE MISSION: Frame work as 'fixing institutional gaps' and 'finding blind spots.'
    3. PRACTICALITY: Use punchy, direct sentences. If you mention a technical skill (SQL/Python), 
       immediately link it to a practical outcome (e.g., 'ensuring families aren't left behind').
    4. RESILIENCE: Subtly weave in the 'Mastery of Logistics' from your USPS days or the 
       'High-Stakes Communication' from Interpreting to show why you master new tools fast.
    5. TARGET: A professional human recruiter who values grit and real-world impact.
    """

    prompt = f"{style_guide}\n\nTASK: Rewrite these STAR bullets to match my voice:\n{draft_text}"

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a blunt, practical career coach refining a first-gen student's resume."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
