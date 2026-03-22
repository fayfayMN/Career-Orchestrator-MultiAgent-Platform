# agents/interviewer.py
from openai import OpenAI

def generate_interview_questions(resume_text, gaps, api_key):
    """
    Agent 6: The Mock Interviewer.
    Generates 3 tough questions: 1 Behavioral, 1 Technical, and 1 'Gap-Bridge' question.
    """
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    prompt = f"""
    ROLE: Senior Data Science Hiring Manager at a Fortune 500 company.
    CONTEXT: You have seen the candidate's resume and identified these specific GAPS: {gaps}
    RESUME: {resume_text}

    TASK: Generate 3 high-stakes interview questions.
    1. THE TECHNICAL GRILL: Ask a deep-dive question about a tool they claim to know (e.g., Python/SQL).
    2. THE GAP TEST: Ask how they would handle a project requiring a tool they DON'T know (from the Gaps list).
    3. THE RESILIENCE CHECK: Ask a STAR-method question about a time they failed or handled a 'blind spot'.

    TONE: Professional, intimidating but fair. No fluff.
    """

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a tough Technical Interviewer."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
