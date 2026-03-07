# 💬 ReplyCraft

A respectful, AI-powered reply coach built with **Streamlit** and **Google Gemini**.  
Paste a chat or upload a screenshot — get 3 charismatic, consent-first reply suggestions instantly.



## 🚀 Why This Project?

This project started as a hands-on experiment to understand how **API integration** works in practice — how to send requests, handle responses, manage errors, and build something real on top of it. What began as "let me try calling an API" quickly evolved into a full-featured app with a polished UI, structured prompts, and retry logic.

Key goals:
- **Learn API Integration** – Understand the full lifecycle of working with an external AI API in a real application
- **Build Something Real** – Go beyond a simple script and create a usable product with a proper UI
- **Consent-First** – Every generated reply prioritizes respect, boundaries, and clear communication
- **Multilingual** – Supports English, Czech, Portuguese, or a mix of all three
- **Screenshot OCR** – Upload a chat screenshot and let Gemini extract the text for you
- **Modular Architecture** – Clean separation of LLM logic, prompts, UI, and core utilities



## 🎯 When to Use This Project

- You're stuck on how to reply to a text
- You want to keep a conversation going naturally
- You need help replying to a dry text without being awkward
- You want to ask someone out in a respectful, low-pressure way
- You're learning about building AI-powered apps with Streamlit & Gemini



## ⚡ Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/Superior-ley597/AI---projekt.git
cd AI---projekt
pip install -r requirements.txt
```

### 2. Set Up Your API Key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=models/gemini-2.5-flash
```

> Get a free API key at [Google AI Studio](https://aistudio.google.com/apikey)

### 3. Run the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.



## 🛠️ Features & Tech Stack

**Core Engine:** Python 3.x, Streamlit  
**AI Model:** Google Gemini (via `google-generativeai`)  
**Image Processing:** Pillow (PIL)  
**Config:** python-dotenv  

### How It Works

1. **Paste a chat** or **upload a screenshot** of your conversation
2. Customize your settings — language, tone, risk level, and goal
3. Gemini generates **3 distinct reply suggestions**, each with a coaching insight
4. Copy your favorite reply and send it 🚀

### Settings

| Setting   | Options                                                                   |
|-----------|---------------------------------------------------------------------------|
| Language  | `en`, `cs`, `pt`, `mix` (one reply per language)                          |
| Tone      | `playful`, `confident`, `funny`, `flirty-but-respectful`, `chill`         |
| Risk      | `safe`, `medium`, `bold`                                                  |
| Goal      | `keep convo going`, `reply to dry text`, `ask a question`, `ask them out` |



## 📂 Project Structure

```text
AI---projekt/
├── app.py                    # Streamlit UI & main application logic
├── src/
│   ├── llm/
│   │   ├── gemini_client.py  # Gemini API wrapper with retry logic
│   │   └── prompts.py        # System instructions & prompt builders
│   ├── core/
│   │   ├── safety.py         # Safety & content filtering
│   │   └── schemas.py        # Response validation schemas
│   └── ui/
│       └── components.py     # Reusable UI components
├── tests/
│   └── test_prompt.py        # Prompt generation tests
├── assets/
│   └── logo.png              # App logo
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```



## 🧠 What I Learned

- How to integrate the **Google Gemini API** into a real application
- Designing **structured prompts** that produce reliable JSON output
- Building interactive web apps with **Streamlit** (tabs, sessions, spinners)
- Implementing **OCR via multimodal AI** — feeding images directly to an LLM
- How to enforce **ethical AI guardrails** (consent-first replies, safety notes)
- Retry patterns and **error handling** for production API calls



## 🛡️ Safety & Ethics

ReplyCraft is built around a core principle: **respect comes first**.

- Every reply is generated with consent-first guidelines
- Manipulative, guilt-tripping, or pressuring language is explicitly forbidden
- A safety note is included whenever the AI detects a sensitive context
- The system instruction enforces clear, kind, and attractive communication



## 👤 Author

High school student learning artificial intelligence and machine learning.
