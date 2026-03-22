# agents/voice_filter.py
from openai import OpenAI

def refine_to_human_voice(draft_text, api_key):
    """
    Agent 4: The Voice Filter.
    Strips AI tone and applies the 'Feifei' style guide.
    """
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    # This prompt uses style markers from your TRIO essay
    style_guide = """
    STYLE GUIDE:
    - Tone: Blunt, practical, and direct[cite: 22, 154].
    - Structure: Short, punchy sentences[cite: 26, 42].
    - Forbidden Words: leverage, synergistic, passionate, delve, multifaceted.
    - Focus: Resilience, finding 'blind spots', and bridging community gaps[cite: 73, 74].
    """

    prompt = f"{style_guide}\n\nTASK: Rewrite the following AI-generated draft to sound like a human who follows this style guide:\n{draft_text}"

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
