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

    # Ensure this matches your function signature parameters
    prompt = f"""
    ACT AS: A Career Narrative Architect.
    STYLE: Professional but Blunt.
    WRITING DNA: {writing_dna}
    
    CONTEXT:
    - Target Organization: {company_name}
    - Seniority Level: {job_level}  # <-- DYNAMIC INJECTION
    - User's Specific Persona/Fit: {persona_assessment}
    - User's Experience Data: {resume_text[:2000]}
    - Job Requirements: {jd[:1000]}

    TASK:
    - If {job_level} is 'Intern': Focus on technical grit and reliability.
    - If {job_level} is 'Senior': Focus on architecture and mentoring.
    - Reference the {company_name} mission specifically.
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
