# agents/storyteller.py
from openai import OpenAI

def draft_star_bullets(resume_data, gap_analysis, target_jd, api_key):
    """
    Agent 3: The Storyteller configured for DeepSeek API.
    Uses the OpenAI library to communicate with DeepSeek's compatible endpoint.
    """
    
    # Configure the client to point to DeepSeek instead of OpenAI
    client = OpenAI(
        api_key=api_key, 
        base_url="https://api.deepseek.com"
    )

    prompt = f"""
    ROLE: Senior Technical Career Coach & Storyteller.
    USER BACKGROUND: {resume_data}
    IDENTIFIED GAPS: {gap_analysis}
    TARGET JOB: {target_jd}

    TASK:
    Generate 3 high-impact bullet points using the STAR method[cite: 159, 295].
    
    CONSTRAINTS:
    1. BRIDGE THE GAP: If a technical gap exists, explain how the user is 'Currently Learning' or how past 'Logistics Reliability' ensures fast mastery[cite: 103, 112].
    2. USE THE HISTORY: Incorporate strengths like USPS operational accuracy or interpreting-based communication[cite: 159, 205].
    3. METRICS MATTER: Ensure every bullet has a quantifiable result (e.g., 99.9% accuracy, 1st Place AGENT.AI)[cite: 159].
    4. VOICE: Be blunt and practical. Avoid AI fluff like 'synergy' or 'passionate'[cite: 75, 207].
    """

    response = client.chat.completions.create(
        model="deepseek-chat",  # This is the ID for DeepSeek-V3
        messages=[
            {"role": "system", "content": "You are a blunt, practical career coach for first-gen students[cite: 75, 138]."},
            {"role": "user", "content": prompt}
        ],
        stream=False
    )
    
    return response.choices[0].message.content
