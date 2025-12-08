import os
import re
import markdown
from openai import OpenAI
from dotenv import load_dotenv

# Load env vars and initialize OpenAI client
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

def _call_gpt(prompt: str, system_prompt: str = "You are a helpful recipe assistant.") -> str:

    if client is None:
        return "<p style='color:orange;'>[GPT disabled in test mode]</p>"
        
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"<p style='color:red;'>Error generating response: {str(e)}</p>"

def generate_recipes_from_ingredients(ingredients: list) -> list:
    prompt = (
        f"Suggest 3 creative recipes using the following ingredients that are about to expire: "
        f"{', '.join(ingredients)}. Each recipe should include a title, ingredients list, and step-by-step instructions."
    )
    raw_output = _call_gpt(prompt)

    # Split by recipe headers like **Recipe 1: ...**
    blocks = re.split(r'(?:^|\n)(?=\*\*Recipe \d+:)', raw_output)

    formatted = []
    for block in blocks:
        clean_block = block.strip()
        if clean_block:
            formatted.append(markdown.markdown(clean_block))

    return formatted
