import json
from openai import OpenAI

def run_strategy_architect(resume, jd, job_level, company_name, api_key):
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    prompt = f"ACT AS: Senior Recruiter... [Logic for {company_name}]" # (Full prompt from previous step)
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            response_format={'type': 'json_object'}
        )
        content = response.choices[0].message.content.strip()
        
        # Log 05: Markdown Sanitizer
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
            
        return json.loads(content)
    except Exception as e:
        return {"error": str(e), "match_score": 0}
