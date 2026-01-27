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
    generate_btn = st.button(
        "Generate replies", 
        type="primary",
        use_container_width=True,
        disabled=disabled_flag
        )
    
def parse_replies(raw: str) -> list[str]:
    lines = [ln.strip() for ln in raw.splitlines() if ln.strip()]
    replies = []

    for ln in lines:
        m = re.match(r"^[123]\)\s*(.*)$", ln)

        if m:
            replies.append(m.group(1).strip())

    return replies[:3]

if generate_btn:
    if not chat_text.strip():
        st.warning("Paste some chat text first.")
    else:
        prompt = build_user_prompt(chat_text, language, tone, risk, goal)

        if st.session_state["last_prompt"] == prompt and st.session_state["last_output"]:
            raw = st.session_state["last_output"]
        else:
            try:
                st.session_state["is_generating"] = True
                with st.spinner("Generating..."):
                    raw = generate_text(prompt, SYSTEM_INSTRUCTION)

                st.session_state["last_prompt"] = prompt
                st.session_state["last_output"]= raw

            except GeminiError as e:
                st.error(str(e))
                raw = None

            except Exception as e:
                st.error(f"Unexpected error: {e}")
                raw = None
            finally:
                st.session_state["is_generating"] = False

        if raw:
            replies = parse_replies(raw)

            st.subheader("Reply suggestions")
            
            if not replies:
                st.warning("I couldn't parse the replies cleanly. Here is the raw output:")
                st.write(raw)
            else:
                for i, r in enumerate(replies, start=1):
                    with st.container(border=True):
                        st.markdown(f"**Option {i}**")
                        st.write(r)
                        st.code(r, language=None)
                        
            if show_debug:
                st.subheader("Prompt (debug)")
                st.code(prompt)

            st.divider()
            st.caption("Tip: If the replies feel off, add more context or paste 2-3 previous messages.")
