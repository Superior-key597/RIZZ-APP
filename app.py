import io
import json
import streamlit as st
from dotenv import load_dotenv
from pathlib import Path
from PIL import Image

from src.llm.prompts import SYSTEM_INSTRUCTION, OCR_SYSTEM_INSTRUCTION, build_user_prompt, build_transcript_prompt
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
    show_debug = st.toggle("Show prompt debug", value=False)

tab_text, tab_image = st.tabs(["📝 Paste Text", "🖼️ Upload Screenshot"])

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

def render_replies(data: dict):
    st.subheader("Reply suggestions")

    for i, r in enumerate(data["replies"], start=1):
        with st.chat_message("assistant"):
            st.markdown(f"**Option {i}** · `{r['lang']}`")
            st.write(r["text"])
            st.info(f"💡 Coach insight: {r['style_note']}")
            
            with st.expander("Copy"):
                st.code(r["text"], language=None)

    safety_note = (data.get("safety_note") or "").strip()
                    
    if safety_note:
        st.warning(f"🛡️ {safety_note}")

def run_generation(chat_text: str, image: Image.Image | None):
    prompt = build_user_prompt(chat_text, language, tone, risk, goal)
    
    cache_key = (prompt, bool(image))
    if st.session_state["last_prompt"] == cache_key and st.session_state["last_output"]:
            raw = st.session_state["last_output"]
    else:
        st.session_state["is_generating"] = True
        try:
            with st.spinner("Generating..."):
                raw = generate_text(prompt, SYSTEM_INSTRUCTION, image=image)

            st.session_state["last_prompt"] = cache_key
            st.session_state["last_output"] = raw
        finally:
            st.session_state["is_generating"] = False

    if show_debug:
        st.subheader("Prompt (debug)")
        st.code(prompt)
        
    try:
        data = safe_json_loads(raw)
        err = validate_payload(data)
        if err:
            st.warning(err)
            st.subheader("Raw model output")
            st.code(raw)
        else:
            render_replies(data)

    except json.JSONDecodeError:
        st.warning("Model did not return valid JSON. Showing raw output:")
        st.code(raw)

with tab_text:
    chat_text = st.text_area("Paste the chat context:", height=220, placeholder="Them: ...\nMe: ...")
    disabled_flag = bool(st.session_state.get("is_generating", False))
    generate_btn = st.button("Generate replies", type="primary", width="stretch", disabled=disabled_flag)

    if generate_btn:
        if not chat_text.strip():
            st.warning("Paste some chat text first.")
        else:
            try:
                run_generation(chat_text, image=None)
            except GeminiError as e:
                st.error(str(e))
            except Exception as e:
                st.error(f"Unexpected error: {e}")

with tab_image:
    st.write("Upload a screenshot of the chat.")

    uploaded = st.file_uploader("Upload screenshot", type=["png", "jpg", "jpeg", "webp"])

    extra_context = st.text_area(
        "Optional context",
        placeholder="e.g., 'I am the blue messages' or 'She is the one on the left'",
        height=68
    )

    disabled_flag = bool(st.session_state.get("is_generating", False))
    generate_image_btn = st.button("Generate", type="primary", width="stretch", disabled=disabled_flag)

    if uploaded is not None:
        img_bytes = uploaded.read()
        pil_img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        st.image(pil_img, caption="Uploaded screenshot", use_container_width=True)
    else:
        pil_img = None

    if generate_image_btn:
        if pil_img is None:
            st.warning("Upload a screenshot first.")
        else:
            try:
                st.session_state["is_generating"] = True

                with st.spinner("Reading screenshot..."):
                    transcript_prompt = build_transcript_prompt(extra_context)
                    transcript = generate_text(transcript_prompt, OCR_SYSTEM_INSTRUCTION, image=pil_img)
                
                st.success("Screenshot read successfully!")

                with st.expander("View Extracted Chat"):
                    st.text(transcript)

                run_generation(chat_text=transcript, image=None)

            except GeminiError as e:
                st.error(str(e))
            except Exception as e:
                st.error(f"Unexpected error: {e}")
            finally:
                st.session_state["is_generating"] = False

