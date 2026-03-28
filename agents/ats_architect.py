from openai import OpenAI
import json

def run_ats_architect(resume_text, jd, persona_summary, writing_dna, job_level, api_key):
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    # The 'Jargon Blacklist' is now a constraint, not a separate agent pass
    blacklist = ["synergy", "spearheaded", "passionate", "leverage", "meticulous", "deep-dive"]

    prompt = f"""
    ACT AS: A Dual-Persona Career Architect. 
    PERSONA 1: A ruthless ATS Optimization Engineer.
    PERSONA 2: A 'Hungry Automator' using this Writing DNA: {writing_dna}.

    CONTEXT: 
    User Persona Assessment: {persona_summary}
    Target Level: {job_level}

    INPUT DATA:
    Master Resume: {resume_text}
    Job Description: {jd}

    PHASE 1: ATS MAPPING
    Identify high-frequency technical keywords from the JD. Map them to the candidate's actual achievements.

    PHASE 2: STAR BULLET CONSTRUCTION (The 'Workhorse' Method)
    Rewrite the experience into bullets. 
    - NO 'corporate ego'. Use 'I fixed the lag' instead of 'I optimized the performance'.
    - NO BLACKLIST WORDS: {', '.join(blacklist)}.
    - DATA IS KING: Must include specific metrics (e.g., 99.9% accuracy, 70k records).

    PHASE 3: SELF-AUDIT
    Review your draft. If it sounds like an AI wrote it, strip the adjectives. Make it punchy.

    OUTPUT FORMAT (STRICT JSON):
    {{
      "optimized_bullets": [
        {{ "Role": "string", "Bullets": ["list of strings"] }}
      ],
      "persona_alignment_score": "1-10",
      "voice_check_notes": "Internal critique of tone"
    }}
    """

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a blunt, technical career engineer. You hate fluff and 'AI-slop'."},
            {"role": "user", "content": prompt}
        ],
        response_format={'type': 'json_object'}
    )
    return response.choices[0].message.content
