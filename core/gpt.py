import os
from openai import OpenAI


OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)


def get_gpt_reminder():
    prompt = "Generate a playful, witty health reminder related to hydration, posture, or taking a break. Keep it under 20 words."
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a friendly health reminder assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.9,
            max_tokens=50
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Reminder error: {e}"
