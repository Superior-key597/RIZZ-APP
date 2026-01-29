import json
import streamlit as st
from dotenv import load_dotenv
from pathlib import Path
import re

from src.llm.prompts import SYSTEM_INSTRUCTION, build_user_prompt
from src.llm.gemini_client import generate_text, GeminiError

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

st.set_page_config(page_title="ReplyCraft", page_icon="💬", layout="centered")
st.title("💬 ReplyCraft")
st.caption("Respectful reply coaching - concise, consent-first, and multilingual.")

if "last_prompt" not in st.session_state:
    st.session_state["last_prompt"] = None

if "last_output" not in st.session_state:
    st.session_state["last_output"] = None

if "is_generating" not in st.session_state:
    st.session_state["is_generating"] = False

with st.sidebar:
    st.header("Settings")
    language = st.selectbox("Language", ["en", "cs", "pt", "mix"], index=0)
    tone = st.selectbox("Tone", ["playful", "confident", "funny", "flirty-but-respectful", "chill"], index=0)
    risk = st.selectbox("Risk level", ["safe", "medium", "bold"], index=0)
    goal = st.selectbox(
        "Goal",
        ["keep convo going", "reply to dry text", "ask a question", "ask them out"],
        index=0
    )

chat_text = st.text_area("Paste the chat context:", height=220, placeholder="Them: ...\nMe: ...")

col1, col2 = st.columns(2)

with col1:
    show_debug = st.toggle("Show prompt debug", value=False)
with col2:
    disabled_flag = bool(st.session_state.get("is_generating", False))
    generate_btn = st.button("Generate replies", type="primary", use_container_width=True, disabled=disabled_flag)
    
def safe_json_loads(text: str) -> dict:
    text = (text or "").strip()

    if text.startswith("```"):
        text = text.strip("`").strip()

        if text.lower().startswith("json"):
            text = text[4:].strip()

    return json.loads(text)

def validate_payload(data: dict) -> str | None:
    if not isinstance(data, dict):
        return "Model output is not a JSON object."
    
    if "replies" not in data or not isinstance(data["replies"], list):
        return "JSON missing 'replies' list."
    
    if len(data["replies"]) != 3:
        return "Expected exactly 3 replies."
    
    for r in data["replies"]:
        if not isinstance(r, dict):
            return "Each reply must be an object."
        
        if "text" not in r or "lang" not in r or "style_note" not in r:
            return "Each reply must include: lang, text, style_note."
        
        if not isinstance(r["text"], str) or not r["text"].strip():
            return "Reply text must be a non-empty string."
        
    return None


if generate_btn:
    if not chat_text.strip():
        st.warning("Paste some chat text first.")
    else:
        prompt = build_user_prompt(chat_text, language, tone, risk, goal)

        if st.session_state["last_prompt"] == prompt and st.session_state["last_output"]:
            raw = st.session_state["last_output"]
        else:
            raw = None
            try:
                st.session_state["is_generating"] = True
                with st.spinner("Generating..."):
                    raw = generate_text(prompt, SYSTEM_INSTRUCTION)

                st.session_state["last_prompt"] = prompt
                st.session_state["last_output"]= raw

            except GeminiError as e:
                st.error(str(e))

            except Exception as e:
                st.error(f"Unexpected error: {e}")
    
            finally:
                st.session_state["is_generating"] = False

        if raw:
            try:
                data = safe_json_loads(raw)
                err = validate_payload(data)
                if err:
                    st.warning(err)
                    st.subheader("Raw model output")
                    st.code(raw)
                else:
                    st.subheader("Reply suggestions")

                    for i, r in enumerate(data["replies"], start=1):
                        with st.container(border=True):
                            st.markdown(f"**Option {i}** · `{r['lang']}`")
                            st.write(r["text"])
                            st.caption(r["style_note"])
                            st.code(r["text"], language=None)

                    safety_note = (data.get("safety_note") or "").strip()
                    
                    if safety_note:
                        st.info(safety_note)

            except json.JSONDecodeError:
                st.warning("Model did not return valid JSON. Showing raw output:")
                st.code(raw)

        if show_debug:
            st.subheader("Prompt (debug)")
            st.code(prompt)
                            
            
