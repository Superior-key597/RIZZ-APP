import os
import time
from google import genai
from google.genai import types

class GeminiError(Exception):
    pass

def generate_text(user_prompt: str, system_instruction: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise GeminiError("Missing GEMINI_API_KEY. Add it to your .env file.")
    
    client = genai.Client(api_key=api_key)

    model_id = os.getenv("GEMINI_MODEL", "models/gemini-2.5-flash")
    
    max_retries = 3
    base_delay = 2

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=model_id,
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.7,
                )
            )

            if not response.text:
                raise GeminiError("Gemini blocked the response (Safety Filters). Try a safer prompt.")
            return response.text
        
        except Exception as e:
            error_msg = str(e)

            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg or "503" in error_msg:
                if attempt < max_retries - 1:
                    wait_time = base_delay * (2 ** attempt)
                    print(f"Server busy. Retrying in {wait_time}s")
                    time.sleep(wait_time)
                    continue
                else:
                    raise GeminiError("Server is busy. Please wait a minute and try again.")
                
            raise GeminiError(f"API Error: {error_msg}")