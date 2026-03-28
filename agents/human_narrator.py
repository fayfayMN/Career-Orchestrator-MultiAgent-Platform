import json
from openai import OpenAI

# STEP 1: Add the missing 'job_level' and 'style_sample' to the signature
def run_human_narrator(resume_text, jd, persona_assessment, writing_dna, company_name, job_level, api_key, style_sample=""):
    """
    Generalized Layer 3: Composer + Voice Filter.
    Matches the 8-argument handshake from app.py.
    """
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    # Jargon Blacklist
    blacklist = ["synergy", "spearheaded", "passionate", "leverage", "meticulous", "deep-dive"]

    # STEP 2: Logic to prioritize the uploaded V1 DNA sample
    style_instruction = f"Mimic the linguistic DNA (sentence structure, tone, 'grit') found in this sample: {style_sample[:1500]}" if style_sample else f"Follow the {writing_dna} style guide."

    prompt = f"""
    ACT AS: A Career Narrative Architect.
    STYLE: Standard Formal Cover Letter.
    WRITING DNA: {writing_dna}
    MANDATE: {style_instruction}
    
    CONTEXT:
    - Target Organization: {company_name}
    - Seniority Level: {job_level}
    - User's Specific Persona: {persona_assessment}
    - User's Experience Data: {resume_text[:2000]}
    - Job Requirements: {jd[:1000]}

    TASK:
    1. THE FORMAT: Write a standard 3-paragraph formal cover letter (Header, Salutation, Body, Closing).
    2. THE ANCHORS: Lead with the 3.9 GPA and #1 AGENT.AI win [cite: 2026-03-04, 2026-01-09].
    3. THE BRIDGE: For {job_level} level, link the 99.9% USPS accuracy to managing 'messy' data pipelines [cite: 2026-03-23, 2026-03-28].
    4. VETO: Strictly avoid these words: {', '.join(blacklist)}.

    OUTPUT FORMAT (STRICT JSON ONLY):
    {{
      "cover_letter_narrative": "Full formal letter content with line breaks...",
      "internal_placement_strategy": "## 🛡️ Internal Verdict\\n- **Assessment:** [Blunt fit for {job_level}]\\n- **Risks:** [Impatience/Culture clash]\\n- **Onboarding:** [Specific tips]",
      "value_anchor": "Link between USPS/AGENT.AI and {company_name}"
    }}
    """

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a blunt career coach. You hate fluff and AI-slop."},
                {"role": "user", "content": prompt}
            ],
            response_format={'type': 'json_object'}
        )
        
        content = response.choices[0].message.content.strip()
        
        # Markdown Sanitizer
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
            
        return json.loads(content)
        
    except Exception as e:
        return {
            "cover_letter_narrative": f"Error generating narrative: {str(e)}",
            "internal_placement_strategy": "Failed",
            "value_anchor": "N/A"
        }
