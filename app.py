import streamlit as st
from src.llm.prompts import build_user_prompt

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

if st.button("Build prompt(debug)", type="primary"):
    if not chat_text.strip():
        st.warning("Paste some chat text first.")
    else:
        prompt = build_user_prompt(
            chat_text=chat_text,
            language=language,
            tone=tone,
            risk=risk,
            goal=goal,
        )
        st.subheader("Generated prompt(debug)")
        st.code(prompt)