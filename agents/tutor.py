from openai import OpenAI

def generate_syllabus(gaps, job_level, api_key):
    """
    Agent 2: The Tutor
    Creates a 48-hour learning sprint focused on the actual job level.
    """
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    # SENIORITY-BASED LEARNING STRATEGY
    if job_level == "Entry/Internship":
        level_instruction = """
        FOCUS: Business Utility and Immediate Support.
        - Prioritize: Excel/Google Sheets mastery, basic SQL, Data Visualization (Tableau/PowerBI), and Process Documentation.
        - AVOID: Production engineering tools like Airflow, Docker, Kubernetes, or Cloud Architecture unless explicitly named in the JD.
        - GOAL: Make the intern useful on Day 1 for manual data tasks.
        """
    elif job_level == "Senior/Specialist":
        level_instruction = """
        FOCUS: Scalability and Architecture.
        - Prioritize: CI/CD pipelines, Orchestration (Airflow), Model Deployment, and System Design.
        - GOAL: High-level technical leadership and ROI.
        """
    else: # Associate/Professional
        level_instruction = """
        FOCUS: Independent Execution.
        - Prioritize: Advanced Python/R, Statistical Modeling, and Database Management.
        - GOAL: Solving specific business problems with data.
        """

    prompt = f"""
    ROLE: Practical Technical Mentor.
    TASK: Create a '48-Hour Learning Sprint' for these specific gaps: {gaps}.
    TARGET LEVEL: {job_level}
    
    STRATEGY:
    {level_instruction}

    FORMAT (Markdown):
    1. THE FUNDAMENTAL: (The 20% of the concept that gives 80% of the results).
    2. THE RESOURCE: (Specific YouTube search terms or documentation links).
    3. THE MINI-PROJECT: (A 2-hour hands-on task to prove competency).
    4. INTERVIEW TALKING POINT: (How to explain this new skill to a recruiter).
    """

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a blunt technical tutor. You teach only what is necessary for the specific job level."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
