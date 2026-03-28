import json
from openai import OpenAI

def run_human_narrator(resume_text, jd, persona, writing_dna, company, job_level, api_key, style_sample=""):
    """
    Dynamic Narrative Architect: Tailors the "OpenAI Standard" to any level.
    """
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    
    # AI-Slop Filter: Removes 'Passionate' and 'Synergy'
    blacklist = ["synergy", "spearheaded", "passionate", "leverage", "vibrant", "dynamic", "medication", "pharma"]

    prompt = f"""
    ACT AS: A Technical Recruiter & Narrative Strategist.
    STRICT RULE: Focus 100% on Business ROI and Technical Efficiency.
    
    CONTEXT:
    - Target: {company} ({job_level})
    - Tech Stack needed in JD: {jd[:1000]}
    - Candidate Evidence: {resume_text[:2000]}

    TASK: Write a 3-paragraph "High-Signal" Cover Letter.

    DYNAMIC LOGIC FOR IMPROVEMENT:
    1. THE HOOK ({job_level}): 
       - If 'Intern/Junior': Focus on GPA, competition wins, and 'Eagerness to contribute' to {company}'s specific tech stack.
       - If 'Senior/Lead': Focus on ROI, team leadership, and architectural vision.
       - THE RUTHLESS HOOK: Do NOT start with "I am writing to...". Start with a 'Headline Achievement'. 
       - e.g., "As the 1st Place winner of the MN AGENT.AI competition, I specialize in transforming raw datasets into executive insights." [cite: 24, 27]
    
    2. CONCRETE TOOL INTEGRATION: You MUST explicitly name 3-4 tools from the JD (e.g., SQL, Power BI, Jira, Python) and link them to a specific project outcome from the resume. [cite: 59, 60, 80, 82]
    
    3. THE BUSINESS PIVOT: Replace "abstract help" with "operational efficiency." 
       - Instead of 'helping people', explain how you 'reduce repeat work', 'ensure data integrity', or 'automate manual reporting'. [cite: 58, 74, 84, 99]
       -  THE ALIGNMENT: Reference {company}'s mission (e.g., 'assembling TVs in the USA' for Element).
       
    4. STAR-BASED PRECISION: Every claim must follow: [Technical Tool] + [Action] = [Measurable Business Result].
       - Search {resume_text} for the candidate's highest quantitative metric (e.g., %, $, #, or ranking).
       - If no metric exists, identify their most significant technical project outcome.
       - PIVOT that specific achievement to solve a core problem found in the {company} JD.

    5. THE TRANSFERABLE BRIDGE: 
       - INSTRUCTION: Identify the candidate's primary domain (e.g., Finance, USPS, or Healthcare) and a core technical method they used (e.g., normalization, predictive modeling).
       - PIVOT: Explain how that specific logic applies to {company}'s specific workflow (e.g., PIM, eCommerce, or Supply Chain).

    6. LEARNING AGILITY: 
       - INSTRUCTION: Search the resume for the candidate's highest academic metric (GPA) and any competitive rankings or awards.
       - APPLICATION: Use these specific numbers as concrete evidence of how fast they will master {company}'s tools and systems.

    VETO: {', '.join(blacklist)}. No long, abstract sentences. Keep it punchy.
    
    OUTPUT FORMAT (STRICT JSON ONLY):
    {{
      "cover_letter_narrative": "Subject: {job_level} Application - {company}\\n\\nDear Hiring Manager,\\n\\n[Para 1: The Technical Headline]\\n\\n[Para 2: Tool-Specific Impact Bridge]\\n\\n[Para 3: Call to Action with Company Mission Alignment]\\n\\nSincerely,\\n\\n[Name]",
      "value_anchor": "Bridge between [Candidate Tool/Metric] and [{company} Operational Problem]."
    }}
    """
    

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "system", "content": "You are a blunt career coach. No fluff."},
                      {"role": "user", "content": prompt}],
            response_format={'type': 'json_object'}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}
