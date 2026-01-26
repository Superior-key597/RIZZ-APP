SYSTEM_INSTRUCTION = """
You are ReplyCraft, a respectful reply-coaching assisstant.
You help users write charismatic, confident replies while prioritizing consent, boundaries, and respect.
You avoid manipulatiton, guilt-tripping, pressure, harassment, or disrespect.
Your goal is to help users communicate clearly, kindly, and attractively.
""".strip()

def build_user_prompt(chat_text: str, language: str, tone: str, risk: str, goal:str) -> str:
    chat_text = chat_text.strip()

    if language == "mix":
        output_rules = """
OUTPUT FORMAT (follow exactly):
1) [EN] <reply in English, max 160 characters>
2) [CS] <reply in Czech, max 160 characters>
3) [PT] <reply in Portuguese, max 160 characters>
""".strip()
    else:
        output_rules = """
OUTPUT FORMAT (follow exactly):
1) <Reply 1, max 160 characters>
2) <Reply 2, max 160 characters>
3) <Reply 3, max 160 characters>
""".strip()

    prompt = f"""
CHAT CONTEXT:
{chat_text}

GOAL:
{goal}

STYLE SETTINGS:
- Language: {language}
- Tone: {tone}
- Risk: {risk}

RULES (very important):
- Write 3 distinct reply options.
- Each reply must be ONE message only (no multi-paragraph).
- Each reply must be <= 160 characters.
- No cringe, no overexplaining, no long compliments.
- Be natural, human, and specific to the chat context.
- Keep it respectful, consent-first, and non-pushy.
- If asking them out: make it easy to say no

{output_rules}
""".strip()
    
    return prompt