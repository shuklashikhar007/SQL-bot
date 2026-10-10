import streamlit as st
from langchain_utils import process_prompt
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="SQLBot - Gen AI DB Manager", page_icon="🤖", layout="wide", initial_sidebar_state="expanded")

# Inject Custom Neo-Brutalist CSS
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700;800;900&family=Space+Mono:ital,wght@0,400;0,700;1,400&display=swap');

/* Global Fonts & Background */
html, body, [class*="css"]  {
    font-family: 'Space Grotesk', sans-serif !important;
}
code, pre, [class*="stChatMessage"] {
    font-family: 'Space Mono', monospace !important;
}

/* App Background (Blueprint Grid) */
.stApp {
    background-color: #f5f4ef;
    background-image: 
        linear-gradient(to right, rgba(0, 0, 0, 0.07) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(0, 0, 0, 0.07) 1px, transparent 1px) !important;
    background-size: 24px 24px !important;
    color: #121212;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background-color: #ffffff;
    border-right: 4px solid #000000;
}
[data-testid="stSidebar"]::before {
    content: "";
    position: absolute;
    top: 0; right: 0; bottom: 0; left: 0;
    pointer-events: none;
    box-shadow: inset -4px 0 0 0 #000000;
}

/* Hide Default Top Header & Footer */
header[data-testid="stHeader"] {
    background-color: transparent !important;
    border-bottom: 4px solid #000000;
    box-shadow: 0 4px 0px rgba(0,0,0,1);
    background: #f5f4ef !important;
}
footer {visibility: hidden;}

/* Brutalist Buttons */
.stButton > button {
    background-color: #38bdf8 !important;
    color: #000000 !important;
    border: 2px solid #000 !important;
    border-radius: 0 !important;
    box-shadow: 4px 4px 0px #000 !important;
    font-weight: 800 !important;
    text-transform: uppercase !important;
    transition: all 0.1s ease !important;
}
.stButton > button:hover {
    transform: translate(-1px, -1px) !important;
    box-shadow: 6px 6px 0px #000 !important;
}
.stButton > button:active {
    transform: translate(3px, 3px) !important;
    box-shadow: 1px 1px 0px #000 !important;
}

/* Chat Input Styling */
[data-testid="stChatInput"] {
    background-color: #000000 !important;
    border: 2px solid #000000 !important;
    box-shadow: 4px 4px 0px #000000 !important;
    border-radius: 0 !important;
}
[data-testid="stChatInput"] textarea {
    font-family: 'Space Mono', monospace !important;
    color: #ffffff !important;
}

/* Chat Messages Default Fallback */
[data-testid="stChatMessage"] {
    background-color: #000000 !important;
    border: 2px solid #000000;
    box-shadow: 4px 4px 0px #000000;
    border-radius: 0;
    padding: 1rem;
    margin-bottom: 1rem;
}

/* User Message (Input to LLM) */
[data-testid="stChatMessage"]:nth-of-type(odd),
[data-testid="stChatMessage"]:has([data-testid*="user"]),
[data-testid="stChatMessage"]:has([aria-label*="user"]) {
    background-color: #000000 !important;
    color: #ffffff !important;
}

/* Assistant Message (Output Box) */
[data-testid="stChatMessage"]:nth-of-type(even),
[data-testid="stChatMessage"]:has([data-testid*="assistant"]),
[data-testid="stChatMessage"]:has([aria-label*="assistant"]) {
    background-color: #000000 !important;
    color: #ffffff !important;
}

/* Force ALL text elements inside the Chat Message Markdown to inherit the parent color */
/* This covers tables (th, td), paragraphs, lists, headers, etc. */
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] * {
    color: inherit !important;
}

/* Exception: We do NOT want to force inherit on Code Blocks or Syntax Highlighting */
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] pre,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] pre *,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] code,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] code * {
    color: initial !important; /* Let syntax highlighting keep its own colors */
}

/* Ensure tables have brutalist borders inside chat */
[data-testid="stChatMessage"] table {
    border: 2px solid inherit !important;
    border-collapse: collapse !important;
    width: 100% !important;
}
[data-testid="stChatMessage"] th, 
[data-testid="stChatMessage"] td {
    border: 1px solid inherit !important;
    padding: 0.5rem !important;
}

/* Alerts / Info Boxes */
.stAlert {
    border: 2px solid #000000 !important;
    border-radius: 0 !important;
    box-shadow: 4px 4px 0px #000000 !important;
    color: #000 !important;
    font-weight: 700 !important;
}
.stAlert [data-testid="stMarkdownContainer"] {
    color: #000 !important;
}
.st-emotion-cache-121r98k, .st-emotion-cache-1g8w2d6 {
    background-color: #eaf8f0 !important; /* Success */
}
.st-emotion-cache-2eb1r1, .st-emotion-cache-1u4wzpm {
    background-color: #ffcccc !important; /* Error */
}

/* Headers */
h1, h2, h3 {
    text-transform: uppercase;
    font-weight: 900 !important;
    letter-spacing: -0.05em;
    color: #000 !important;
}

/* Top bar replacement styling */
.neo-header {
    background-color: #f5f4ef;
    border-bottom: 4px solid #000000;
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: -6rem -4rem 2rem -4rem; /* offset streamlit defaults */
    box-shadow: 0 4px 0px #000000;
    position: relative;
    z-index: 50;
}
.sticker {
    display: inline-block;
    transform: rotate(-1.5deg);
    background: #38bdf8;
    border: 2px solid #000;
    padding: 0.25rem 0.75rem;
    box-shadow: 4px 4px 0px #000;
    font-family: 'Space Mono', monospace;
    font-weight: 900;
    font-size: 0.8rem;
    text-transform: uppercase;
}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Custom Top Header via Markdown
st.markdown("""
<div style="display: flex; align-items: flex-end; justify-content: space-between; padding-bottom: 1rem; border-bottom: 2px solid rgba(0,0,0,0.2); margin-bottom: 2rem;">
    <div>
        <div style="display: flex; gap: 12px; align-items: center; margin-bottom: 8px;">
            <div class="sticker">⚡ NATURAL LANGUAGE → SQL</div>
            <span style="font-family: 'Space Mono'; font-size: 0.75rem; background: #fff; border: 1px solid #000; padding: 2px 6px;">AUTONOMOUS QUERY REWRITER</span>
        </div>
        <h1 style="margin: 0; font-size: 2.5rem; line-height: 1;">SQLBot <span style="color: #888;">///</span> Gen AI DB Manager</h1>
        <p style="font-family: 'Space Mono'; font-size: 0.875rem; margin-top: 8px; max-width: 800px;">Direct connection to your Neon PostgreSQL cluster. Generate bulletproof migrations, optimize queries, and manipulate relational data through prompts.</p>
    </div>
    <div style="display: flex; gap: 8px; align-items: center;">
        <span style="font-family: 'Space Mono'; font-size: 0.75rem; font-weight: bold;">ENVIRONMENT:</span>
        <div style="background: #10b981; color: #000; border: 2px solid #000; font-family: 'Space Mono'; font-size: 0.75rem; font-weight: bold; padding: 4px 10px; box-shadow: 2px 2px 0px #000;">
            PRODUCTION_LIVE
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# Sidebar Configuration panel (Neo-Brutalist)
groq_key = os.environ.get("GROQ_API_KEY")
neon_url = os.environ.get("NEON_DATABASE_URL")

with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 8px; border-bottom: 2px solid #000; padding-bottom: 12px; margin-bottom: 16px;">
        <div style="width: 12px; height: 12px; background: #ef4444; border: 1px solid #000;"></div>
        <div style="width: 12px; height: 12px; background: #facc15; border: 1px solid #000;"></div>
        <div style="width: 12px; height: 12px; background: #10b981; border: 1px solid #000;"></div>
        <h2 style="font-family: 'Space Mono'; font-size: 0.875rem; margin: 0; margin-left: 4px;">CONFIG_STATUS</h2>
    </div>
    """, unsafe_allow_html=True)
    
    if groq_key:
        st.success("✅ Groq API Key is SET")
    else:
        st.error("❌ Groq API Key MISSING")
        
    if neon_url:
        st.success("✅ Neon DB URL is SET")
    else:
        st.error("❌ Neon DB URL MISSING")
        
    st.info("💡 Ensure your credentials are set in .env before prompting.")

    st.markdown("""
    <div style="margin-top: 24px; border-top: 1px dashed #000; padding-top: 16px; display: grid; grid-template-columns: 1fr 1fr; gap: 8px; text-align: center; font-family: 'Space Mono';">
        <div style="background: #f5f5f5; border: 1px solid #000; padding: 8px;">
            <span style="font-size: 0.65rem; color: #666; font-weight: bold; display: block;">ENGINE</span>
            <span style="font-size: 0.9rem; font-weight: bold;">QWEN 27B</span>
        </div>
        <div style="background: #f5f5f5; border: 1px solid #000; padding: 8px;">
            <span style="font-size: 0.65rem; color: #666; font-weight: bold; display: block;">LATENCY</span>
            <span style="font-size: 0.9rem; font-weight: bold; color: #10b981;">24ms</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Main Application Window Header
st.markdown("""
<div style="background: #38bdf8; border: 3px solid #000; padding: 8px 16px; display: flex; justify-content: space-between; align-items: center; margin-bottom: -10px; z-index: 10; position: relative;">
    <div style="display: flex; gap: 8px;">
        <span style="width: 12px; height: 12px; background: #ef4444; border: 2px solid #000;"></span>
        <span style="width: 12px; height: 12px; background: #facc15; border: 2px solid #000;"></span>
        <span style="width: 12px; height: 12px; background: #10b981; border: 2px solid #000;"></span>
        <span style="font-family: 'Space Mono'; font-weight: 900; font-size: 0.75rem; margin-left: 8px;">PROMPT_RUNNER.PY</span>
    </div>
    <div style="background: #fff; border: 2px solid #000; font-family: 'Space Mono'; font-weight: bold; font-size: 0.7rem; padding: 2px 8px;">
        MODE: SCHEMA_MUTATION
    </div>
</div>
""", unsafe_allow_html=True)

# Container for chat interface to simulate the "window" styling
with st.container():
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    prompt = st.chat_input("Enter natural language instruction (e.g., Create a users table...)")
    
    if prompt:
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        if not groq_key or not neon_url:
            error_msg = "⚠️ Please configure your `.env` file with `GROQ_API_KEY` and `NEON_DATABASE_URL`."
            with st.chat_message("assistant"):
                st.error(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
        else:
            with st.chat_message("assistant"):
                with st.spinner("Compiling SQL..."):
                    response = process_prompt(prompt)
                st.markdown(response)
                
            st.session_state.messages.append({"role": "assistant", "content": response})

