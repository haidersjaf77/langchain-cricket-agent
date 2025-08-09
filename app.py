import streamlit as st
import random
import time
from db import init_db, add_user, validate_user, save_convo, get_user_history
from chat_agent import get_gemini_response

st.set_page_config(page_title="Cooking...", layout="centered")
st.markdown("""
    <style>
        .futuristic-header {
            font-size: 2.2em;
            font-weight: 900;
            text-align: center;
            color: #00ADB5;
            margin-bottom: 0.2em;
            font-family: 'Segoe UI', sans-serif;
        }
        .tagline {
            font-size: 0.95em;
            text-align: center;
            color: #888888;
            font-style: italic;
            margin-top: -5px;
        }
    </style>
    <div class="futuristic-header">⏳🏏 The 3rd Umpire</div>
""", unsafe_allow_html=True)

init_db()

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "history" not in st.session_state:
    st.session_state.history = []

# Auth logic
def login_ui():
    st.markdown("""
        <style>
            .centered-title {
                text-align: center;
                font-size: 2em;
                font-weight: 700;
                color: #00FFF7;
                text-shadow: 0 0 8px #00FFF7;
            }
            .info-text {
                font-size: 0.95em;
                color: #CFCFCF;
                margin-bottom: 10px;
            }
            .success-text {
                color: #00ff9f;
            }
            .warning-text {
                color: #ffcc00;
            }
            .error-text {
                color: #ff4b4b;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='centered-title'>🧑‍⚖️ The 3rd Umpire Access Portal</div>", unsafe_allow_html=True)
    st.markdown("<p class='info-text' style='text-align:center;'>🎙️ Talk cricket with an AI that knows the game inside out!</p>", unsafe_allow_html=True)

    tabs = st.tabs(["🏏 Sign In", "🆕 Join the Squad"])

    with tabs[0]:
        st.markdown("#### 🏏 Log in to your dugout")
        login_user = st.text_input("🧢 Player Name", key="login_user")
        login_pass = st.text_input("🧤 Secret Code", type="password", key="login_pass")
        login_click = st.button("🟢 Step onto the field")

        if login_click:
            if validate_user(login_user, login_pass):
                st.session_state.logged_in = True
                st.session_state.username = login_user
                st.success("✅ You're in! The innings has begun 🎉")
                st.rerun()
            else:
                st.markdown("<p class='error-text'>🚫 LBW! Wrong player name or code. Review and try again.</p>", unsafe_allow_html=True)

    with tabs[1]:
        st.markdown("#### 🆕 Create your player profile")
        st.markdown("<p class='info-text'>📝 Join the playing XI — pick your name and set a secret code. Then head back to Sign In and take strike!</p>", unsafe_allow_html=True)

        signup_user = st.text_input("🏏 Choose Player Name", key="signup_user")
        signup_pass = st.text_input("🛡️ Set Your Secret Code", type="password", key="signup_pass")
        signup_click = st.button("🏗️ Build My Profile")

        if signup_click:
            if signup_user and signup_pass:
                try:
                    add_user(signup_user, signup_pass)
                    st.markdown("<p class='success-text'>🎉 Player added to the squad! Switch to Sign In to start your innings.</p>", unsafe_allow_html=True)
                except:
                    st.markdown("<p class='error-text'>🛑 That name's already on the team sheet. Pick another one!</p>", unsafe_allow_html=True)
            else:
                st.markdown("<p class='warning-text'>⚠️ Both name and code are required to join the squad.</p>", unsafe_allow_html=True)

# Chat UI with updated typing effect
def chat_ui():
    st.markdown("""
        <style>
            .cricket-header {
                font-size: 2em;
                font-weight: 700;
                color: #00FFF7;
                text-align: center;
                margin-bottom: 10px;
                text-shadow: 0 0 10px #00FFF7;
            }
            .chatbox {
                background-color: #0A192F;
                padding: 20px;
                border-radius: 10px;
                margin: 10px 0;
            }
            .user-msg {
                color: #FFD700;
            }
            .ai-msg {
                color: #00ff9f;
                font-style: italic;
            }
            .typing {
                color: #ffffffaa;
                font-style: italic;
                animation: blink 1s infinite;
            }
            @keyframes blink {
                0% { opacity: 0.2; }
                50% { opacity: 1; }
                100% { opacity: 0.2; }
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(f"<div class='cricket-header'>🏏 Welcome to The 3rd Umpire, {st.session_state.username}! 🧠</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Ask about anything cricket — rules, legends, matches, or controversies!</p>", unsafe_allow_html=True)

    # Display chat history
    for msg, reply in get_user_history(st.session_state.username):
        with st.chat_message("user"):
            st.markdown(f"<div class='chatbox user-msg'>🧍‍♂️ {msg}</div>", unsafe_allow_html=True)
        with st.chat_message("ai"):
            st.markdown(f"<div class='chatbox ai-msg'>🤖 {reply}</div>", unsafe_allow_html=True)

    # New user input
    user_input = st.chat_input("🏏 What's your cricket question today?")

    if user_input:
        with st.chat_message("user"):
            st.markdown(f"<div class='chatbox user-msg'>🧍‍♂️ {user_input}</div>", unsafe_allow_html=True)

        with st.chat_message("ai"):
            placeholder = st.empty()

            # Typing effect with random phrases
            typing_phrases = [
                "Analyzing the pitch... 🧐",
                "Watching the replay... 🎬",
                "Consulting Hawk-Eye... 🎯",
                "Checking Snickometer... 🎧",
                "Calling upstairs... ☎️"
            ]
            typing_text = random.choice(typing_phrases)
            placeholder.markdown(
                f"<div class='chatbox ai-msg typing'>🤖 {typing_text}</div>",
                unsafe_allow_html=True
            )

            time.sleep(1.5)

            # Get Gemini response
            response = get_gemini_response(user_input, st.session_state.username)
            response_text = response.content.strip()

            # Show final response
            placeholder.markdown(f"<div class='chatbox ai-msg'>🤖 {response_text}</div>", unsafe_allow_html=True)

        # Save conversation
        save_convo(st.session_state.username, user_input, response_text)

# App flow
if not st.session_state.logged_in:
    login_ui()
else:
    chat_ui()