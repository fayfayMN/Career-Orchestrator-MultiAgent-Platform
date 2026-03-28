def run_human_narrator(resume_text, jd, persona_assessment, writing_dna, company_name, api_key):
    """
    Consolidated Layer 3: Composer + Voice Filter
    Generalized for any background (Data Science, Healthcare, USPS, etc.)
    """
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    # Jargon Blacklist to ensure 'Human' quality for all users
    blacklist = ["synergy", "spearheaded", "passionate", "leverage", "meticulous", "deep-dive"]

    prompt = f"""
    ACT AS: A Career Narrative Architect.
    STYLE: Professional but Blunt. No 'AI-slop'.
    WRITING DNA: {writing_dna}
    
    CONTEXT:
    - Target Organization: {company_name}
    - User's Unique Persona Traits: {persona_assessment}
    - User's Master History: {resume_text[:2000]}
    - Job Requirements: {jd[:1000]}

    TASK:
    1. THE HOOK: Start with a hard achievement or specialized skill from the resume that directly solves a pain point in the JD. No 'I am writing to express interest.'
    2. THE BRIDGE: Use the 'User Persona' traits to explain how their non-linear background (the 'Value Anchor') makes them more reliable than a 'standard' candidate.
    3. THE 'MESS' RULE: Use punchy, direct language. Use contractions. Replace corporate jargon with 'Workhorse' vocabulary (e.g., use 'handled' instead of 'orchestrated').
    4. VETO: If you use any words from this blacklist ({', '.join(blacklist)}), rewrite the sentence.

    OUTPUT FORMAT (STRICT JSON):
    {{
      "cover_letter_narrative": "The full text",
      "voice_audit": "Explanation of how the tone matches the Writing DNA",
      "value_anchor": "The specific unique trait used to bridge the background to the role"
    }}
    """

    response = client.chat.completions.create(
        model="deepseek-chat", # Tier 2 (Language) for cost-efficiency
        messages=[
            {"role": "system", "content": "You are a blunt technical writer. You hate fluff."},
            {"role": "user", "content": prompt}
        ],
        response_format={'type': 'json_object'}
    )
    return response.choices[0].message.content
