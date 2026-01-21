import streamlit as st
from dotenv import load_dotenv
from pathlib import Path
import os

from src.llm.prompts import SYSTEM_INSTRUCTION, build_user_prompt
from src.llm.gemini_client import generate_text, GeminiError

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

st.set_page_config(page_title="ReplyCraft", page_icon="💬")
st.title("💬 ReplyCraft")

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

chat_text = st.text_area("Paste chat text:", height=220, placeholder="Them: ...\nMe: ...")

if "last_prompt" not in st.session_state:
    st.session_state.last_prompt = None

if "last_output" not in st.session_state:
    st.session_state.last_output = None

if "is_generating" not in st.session_state:
    st.session_state.is_generating = None

col1, col2 = st.columns(2)

with col1:
    build_prompt_btn = st.button("Build prompt(debug)", use_container_width=True)
with col2:
    generate_btn = st.button("Generate (Gemini)", type="primary", use_container_width=True, disabled=st.session_state.is_generating)

if build_prompt_btn:
    if not chat_text.strip():
        st.warning("Paste some chat text first.")
    else:
        prompt = build_user_prompt(chat_text, language, tone, risk, goal)
        st.subheader("Generated Prompt (debug)")
        st.code(prompt)

if generate_btn:
    if not chat_text.strip():
        st.warning("Paste some chat text first.")
    else:
        prompt = build_user_prompt(chat_text, language, tone, risk, goal)

        if st.session_state.last_prompt == prompt and st.session_state.last_output:
            st.subheader("Model output (cached)")
            st.write(st.session_state.last_output)
        else:
            try:
                st.session_state.is_generating = True
                with st.spinner("Generating..."):
                    result = generate_text(prompt, SYSTEM_INSTRUCTION)

                st.session_state.last_prompt = prompt
                st.session_state.last_output = result

                st.subheader("Model output (raw)")
                st.write(result)
            
            except GeminiError as e:
                st.error(str(e))

            except Exception as e:
                st.error(f"Unexpected error: {e}")

            finally:
                st.session_state.is_generating = False
