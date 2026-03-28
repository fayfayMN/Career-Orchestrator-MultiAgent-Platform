import json
from openai import OpenAI

def run_human_narrator(resume_text, jd, persona_assessment, writing_dna, company_name, api_key):
    """
    Generalized Layer 3: Composer + Voice Filter.
    No longer anchored to specific USPS/DS traits—now builds a bridge 
    for ANY user based on their provided persona data.
    """
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    # Jargon Blacklist: The "AI-Slop" filter for professional humans
    blacklist = ["synergy", "spearheaded", "passionate", "leverage", "meticulous", "deep-dive"]

    prompt = f"""
    ACT AS: A Career Narrative Architect.
    STYLE: Professional but Blunt. No 'AI-slop'.
    WRITING DNA: {writing_dna}
    
    CONTEXT:
    - Target Organization: {company_name}
    - User's Specific Strengths/Persona: {persona_assessment}
    - User's Experience Data: {resume_text[:2000]}
    - Job Requirements: {jd[:1000]}

    TASK:
    1. THE HOOK: Start with a quantifiable achievement or high-value technical skill from the user's resume that directly addresses a pain point in the JD. No generic openings.
    2. THE DYNAMIC BRIDGE: Use the 'User's Specific Strengths' to explain how their background—whatever it may be—provides a unique advantage (the 'Value Anchor') for this specific role.
    3. THE 'WORKHORSE' RULE: Use direct, punchy language. Replace corporate jargon with practical, action-oriented vocabulary (e.g., 'handled', 'solved', 'built').
    4. VETO: Strictly avoid these words: {', '.join(blacklist)}.

    OUTPUT FORMAT (STRICT JSON ONLY):
    {{
      "cover_letter_narrative": "string",
      "voice_audit": "Critique of how the narrative matches the requested style",
      "value_anchor": "The specific link identified between the user's past and this role"
    }}
    """

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a blunt career coach. You hate fluff."},
                {"role": "user", "content": prompt}
            ],
            response_format={'type': 'json_object'}
        )
        
        content = response.choices[0].message.content.strip()
        
        # Log 05: Universal Markdown Sanitizer
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
            
        return json.loads(content)
        
    except Exception as e:
        return {
            "cover_letter_narrative": f"Error generating narrative: {str(e)}",
            "voice_audit": "Failed",
            "value_anchor": "N/A"
        }
