import json

SYSTEM_INSTRUCTION = """
You are ReplyCraft, a respectful reply-coaching assisstant.
You help users write charismatic, confident replies while prioritizing consent, boundaries, and respect.
Avoid manipulatiton, guilt-tripping, pressure, harassment, or disrespect.
Your goal is to help users communicate clearly, kindly, and attractively.
Return STRICT JSON only. No markdown. No extra text.
""".strip()

def build_user_prompt(chat_text: str, language: str, tone: str, risk: str, goal:str) -> str:
    chat_text = chat_text.strip()

    schema = {
        "language-mode": "en|cs|pt|mix",
        "tone": "playful|confident|funny|flirty-but-respectful|chill",
        "risk": "safe|medium|bold",
        "goal": "keep convo going|reply to dry text|ask a question|ask them out",
        "replies": [
            {
                "lang": "EN|CS|PT",
                "text": "string (<=160 chars)",
                "style_note": "string (very short, why this fits tone/goal)"
            },
            {
                "lang": "EN|CS|PT",
                "text": "string (<=160 chars)",
                "style_note": "string"
            },
            {
                "lang": "EN|CS|PT",
                "text": "string (<=160 chars)",
                "style_note": "string"
            }    
        ],
        "safety:note": "string (short, consent/respect reminder if relevant)"
    }

    lang_rule = ""
    if language == "mix":
        lang_rule = "- Language mode is mix: produce exactly 3 replies with lang tags EN, CS, PT (one each)."
    else:
        lang_rule = "- Language mode is single: all 3 replies must be in the selected language."

    prompt = f"""
CHAT CONTEXT:
{chat_text}

SETTINGS:
- language_mode: {language}
- tone: {tone}
- risk: {risk}
- goal: {goal}

RULES (must follow):
- Produce exactly 3 distinct replies.
- Each reply must be ONE message only, <= 160 characters.
- No cringe, no overexplaining, no long compliments.
- Be natural, human, and specific to the chat context.
- Keep it respectful, consent-first, and non-pushy.
- If goal is "ask them out", make it easy to say no.
{lang_rule}
- Return STRICT JSON that matches the schema exactly (double quotes, no trailing commmas).
- Output ONLY the JSON (no markdown, no commentary).

SCHEMA:
{json.dumps(schema, ensure_ascii=False)}
""".strip()
    
    return prompt