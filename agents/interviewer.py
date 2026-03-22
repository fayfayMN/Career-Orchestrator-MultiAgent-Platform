# agents/interviewer.py
from openai import OpenAI

def generate_interview_questions(resume_text, gaps, api_key):
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    prompt = f"""
    ROLE: Senior Data Science Hiring Manager.
    CONTEXT: Candidate GAPS: {gaps}. RESUME: {resume_text}

    TASK: Generate 3 high-stakes interview questions:
    1. THE TECHNICAL GRILL: Deep-dive into a tool they claim to know (e.g., Python/SQL).
    2. THE GAP TEST: How they would handle a project requiring a tool they DON'T know (from the Gaps list).
    3. THE RESILIENCE CHECK: A STAR-method question about handling a 'blind spot' or failure.

    TONE: Professional, intimidating but fair. Blunt.
    """

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "system", "content": "You are a tough Technical Interviewer."},
                  {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def evaluate_answer(question, answer, api_key):
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    prompt = f"QUESTION: {question}\nANSWER: {answer}\n\nGrade this answer 1-10. Provide 'Blunt Feedback' on technical accuracy and STAR method structure."
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "system", "content": "You are a blunt Interview Evaluator."},
                  {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
