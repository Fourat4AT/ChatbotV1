import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="Chat with Gemini-Flash!",
    page_icon="⚡", 
    layout="centered"
)

# Get API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  # Changed to match your key name

# Check for API key
if not GOOGLE_API_KEY:
    st.error("❌ GEMINI_API_KEY not found in .env file")
    st.stop()

# Configure Gemini
try:
    gen_ai.configure(api_key=GOOGLE_API_KEY)
except Exception as e:
    st.error(f"❌ Failed to configure Gemini: {e}")
    st.stop()

# Initialize the model - USING GEMINI 2.0 FLASH
try:
    model = gen_ai.GenerativeModel('gemini-1.5-flash')  # Updated model name
except Exception as e:
    st.error(f"❌ Failed to load model: {e}")
    st.stop()

# Function to translate roles for Streamlit
def translate_role(role):
    return "assistant" if role == "model" else role

# Initialize chat session
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# App title
st.title("⚡ Gemini Flash Chatbot")

# Display chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role(message.role)):
        st.markdown(message.parts[0].text)

# User input
user_prompt = st.chat_input("Ask Gemini-Flash...")

if user_prompt:
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_prompt)
    
    try:
        # Get response from Gemini
        response = st.session_state.chat_session.send_message(user_prompt)
        
        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(response.text)
            
    except Exception as e:
        st.error(f"⚠️ Error: {e}")