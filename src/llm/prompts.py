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
OUTPUT:
Return exactly 3 replies in this exact format:
1) [EN] <reply in English>
2) [CS] <reply in Czech>
3) [PT] <reply in Portuguese>
""".strip()
    else:
        output_rules = """
OUTPUT:
Return exactly:
1) Reply 1
2) Reply 2
3) Reply 3
""".strip()

    prompt = f"""
CHAT CONTEXT (what I am replying to):
{chat_text}

TASK:
Write 3 reply options.

SETTINGS:
- Language: {language}
- Tone: {tone}
- Risk: {risk}
- Goal: {goal}

RULES:
- Each reply must be short (max ~2 sentences).
- Be respectful, consent-first, and non-pushy.
- If the goal is "ask them out", make it easy for them to say no.

{output_rules}
""".strip()
    return prompt