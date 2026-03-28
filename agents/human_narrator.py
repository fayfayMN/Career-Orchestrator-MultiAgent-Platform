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
    ACT AS: A Senior Executive Career Coach.
    STYLE: Professional, Formal, and Blunt.
    MANDATE: {style_instruction} # Using your uploaded V1 DNA
    
    CONTEXT:
    - Target: {company_name} | Role: {job_level}
    - Key Wins: 1st Place AGENT.AI, 99.9% USPS Accuracy, 3.9 GPA [cite: 2026-01-09, 2026-03-23, 2026-03-04].

    TASK: Write a standard, formal cover letter. Follow this EXACT structure:
    1. SUBJECT LINE: Reference the {job_level} role and specific team (e.g., A3 Team).
    2. SALUTATION: Professional greeting.
    3. PARAGRAPH 1 (THE HOOK): Directly link the #1 state ranking in AGENT.AI and 3.9 GPA to their need for 'production-ready' data pipelines [cite: 2026-01-09].
    4. PARAGRAPH 2 (THE GRIZZLED BRIDGE): Use the 7 years at USPS and 99.9% accuracy to prove 'Operational Discipline' in managing messy, multi-source data [cite: 2026-03-23].
    5. PARAGRAPH 3 (THE MISSION): Connect bilingual skills and interest in medication access to the {company_name} team culture [cite: 2026-03-28].
    6. CLOSING: Professional sign-off.

    VETO WORDS: {', '.join(blacklist)}.

    OUTPUT FORMAT (STRICT JSON ONLY):
    {{
      "cover_letter_narrative": "Subject: ...\\n\\nDear Hiring Manager,\\n\\n[Paragraph 1]\\n\\n[Paragraph 2]\\n\\n[Paragraph 3]\\n\\nSincerely,\\n\\n[Your Name]",
      "internal_placement_strategy": "## 🛡️ Internal Verdict\\n- **Assessment:** [Blunt fit]\\n- **Risks:** [Impatience/Bluntness]\\n- **Onboarding:** [Specific tips]",
      "value_anchor": "Link between USPS reliability and Data Management"
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
