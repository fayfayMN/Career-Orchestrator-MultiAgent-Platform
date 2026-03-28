import json
from openai import OpenAI

# STEP 1: Add the missing 'job_level' and 'style_sample' to the signature
# agents/human_narrator.py
import json
from openai import OpenAI

def run_human_narrator(resume_text, jd, persona_assessment, writing_dna, company_name, job_level, api_key, style_sample=""):
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    
    # AI-Slop Filter
    blacklist = ["synergy", "spearheaded", "passionate", "leverage", "meticulous", "vibrant", "dynamic"]

    prompt = f"""
    ACT AS: The user, writing a formal letter. 
    Linguistic DNA Template: {style_sample[:1500] if style_sample else writing_dna}
    
    MANDATE:
    1. MIMIC the sentence structure, bluntness, and vocabulary of the 'Linguistic DNA Template'.
    2. USE the 3.9 GPA and #1 AGENT.AI win as technical proof [cite: 2026-03-04, 2026-01-09].
    3. BRIDGE the 7-year USPS discipline (99.9% accuracy) to {company_name}'s need for error-free medication data [cite: 2026-03-23, 2026-03-28].

    TASK: Write a 3-paragraph formal letter. 
    Paragraph 1: The 'Technical Rigor' hook.
    Paragraph 2: The 'Operational Discipline' bridge (USPS focus).
    Paragraph 3: The 'Mission' alignment (Healthcare access).

    VETO: Strictly avoid {', '.join(blacklist)}.

    OUTPUT (STRICT JSON):
    {{
      "cover_letter_narrative": "Subject: Intern Application - Data Science (A3 Team)\\n\\nDear Hiring Manager,\\n\\n[Para 1]\\n\\n[Para 2]\\n\\n[Para 3]\\n\\nSincerely,\\n\\n[Name]",
      "internal_placement_strategy": "## 🛡️ V1 Internal Verdict\\n- **Fit:** [Blunt summary]\\n- **Risks:** [e.g. Impatience/Directness]",
      "value_anchor": "Bridge between USPS reliability and Pharma Data Integrity"
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
