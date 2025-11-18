import streamlit as st
import google.generativeai as genai
from datetime import datetime
from dotenv import load_dotenv
import os;

load_dotenv()

# ---------------------------
# Page setup
# ---------------------------
st.set_page_config(page_title="Astral_X - Chat Bot", page_icon="🤖")
st.markdown("# 🤖 Astral_X - Chat Bot")
st.sidebar.markdown("### Astral_X - Your Friendly ChatBot")

# ---------------------------
# Configure Google API Key
# ---------------------------
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  # Replace with your key
genai.configure(api_key=GOOGLE_API_KEY)

# ---------------------------
# Initialize Gemini Model
# ---------------------------
geminiModel = genai.GenerativeModel("gemini-2.5-flash")
chat = geminiModel.start_chat(history=[])

# ---------------------------
# Function to get response
# ---------------------------
def get_gemini_response(query):
    """Send user query to Gemini and return response."""
    response = chat.send_message(query, stream=True)
    return response

# ---------------------------
# Initialize chat history
# ---------------------------
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

latest_response = ""  # To display the latest bot response outside

# ---------------------------
# User input and buttons
# ---------------------------
user_input = st.text_input("You:", key="input")
submit = st.button("Get Answer")
clear = st.button("Clear Chat")   # Clear button

# ---------------------------
# Clear chat history
# ---------------------------
if clear:
    st.session_state['chat_history'] = []
    st.rerun()  # refresh the app to clear everything

# ---------------------------
# Handle user input
# ---------------------------
if submit and user_input:
    output = get_gemini_response(user_input)
    
    bot_response_text = ""
    for chunk in output:
        bot_response_text += chunk.text
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Store both user and bot message together with timestamp
    st.session_state['chat_history'].append({
        "timestamp": timestamp,
        "user": user_input,
        "bot": bot_response_text
    })
    
    latest_response = bot_response_text

# ---------------------------
# Display latest bot response outside chat history
# ---------------------------
if latest_response:
    st.subheader("🤖 Astral_X's Response:")
    st.write(latest_response)

# ---------------------------
# Display chat history in single collapsible boxes per turn
# ---------------------------
with st.expander("📜 Chat History", expanded=True):
    for idx, entry in enumerate(st.session_state['chat_history']):
        title = f"💬 Chat {idx+1} - {entry['timestamp']}"
        with st.expander(title, expanded=False):
            st.markdown(f"**You:** {entry['user']}")
            st.markdown(f"**Astral_X:** {entry['bot']}")