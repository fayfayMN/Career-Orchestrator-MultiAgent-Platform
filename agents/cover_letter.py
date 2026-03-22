# agents/cover_letter.py
from openai import OpenAI

def generate_cover_letter(resume, jd, narrative, api_key):
    """
    Agent 8: The Cover Letter Composer.
    Uses the Resilience Narrative to build a formal application letter.
    """
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    prompt = f"""
    ROLE: Professional Career Coach.
    TASK: Write a formal 3-paragraph cover letter using the following data:
    
    1. RESUME SUMMARY: {resume[:500]}...
    2. JOB DESCRIPTION: {jd[:500]}...
    3. RESILIENCE NARRATIVE: {narrative}

    STRUCTURE:
    - Paragraph 1: The Hook. Mention the specific role and why your technical background (3.9 GPA) fits.
    - Paragraph 2: The Bridge. Use the 'Resilience Narrative' to explain how your unique path (USPS/Interpreting) prepared you to solve their 'blind spots'.
    - Paragraph 3: The Closing. Call to action and professional sign-off.

    TONE: Confident, blunt, and practical. No AI fluff.
    """

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "system", "content": "You are a professional business writer."},
                  {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
