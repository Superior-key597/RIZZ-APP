import os
from google import genai

class GeminiError(Exception):
    pass

def generate_text(user_prompt: str, system_instruction: str) -> str:
    """
    Minimal Gemini call:
    - takes a user prompt and a system instruction
    - returns raw text
    """

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise GeminiError("Missing GEMINI_API_KEY. Add it to your .env file.")
    
    model = os.getenv("GEMINI MODEL", "gemini-2.0-flash")
    client = genai.Client(api_key=api_key)

    resp = client.models.generate_content(
        model=model,
        contents = user_prompt,
        config = {
            "system_instruction" : system_instruction,
            "temperature" : 0.7
        }
    )

    text = (resp.text or "").strip()
    if not text:
        raise GeminiError("Gemini returned an empty response.")
    return text