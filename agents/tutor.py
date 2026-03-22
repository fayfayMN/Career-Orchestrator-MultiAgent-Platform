# agents/tutor.py
from openai import OpenAI

def generate_syllabus(gap_list, api_key):
    """
    Agent 2: The Tutor.
    For every missing skill, it generates a 'How to Learn This Fast' guide.
    """
    client = OpenAI(
        api_key=api_key, 
        base_url="https://api.deepseek.com"
    )

    prompt = f"""
    ROLE: Senior Data Science Mentor.
    INPUT: A list of technical skill gaps identified in a job audit: {gap_list}
    
    TASK:
    For each gap, create a '48-Hour Learning Syllabus' that includes:
    1. THE FUNDAMENTAL: The one core concept to master first.
    2. THE RESOURCE: Suggest the best documentation (e.g., 'Official Snowflake Docs') or a specific YouTube search term.
    3. THE MINI-PROJECT: A 2-hour coding task to prove basic proficiency (e.g., 'Build a simple ETL pipeline').
    
    GOAL: Enable the user to honestly say: 'I saw you use X; I spent the last 48 hours building a replica pipeline to understand the logic.'
    
    TONE: Encouraging, practical, and time-sensitive.
    """

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a Mentor who bridges the gap between 'I don't know it' and 'I am learning it'."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content
