import streamlit as st
from openai import OpenAI
from supabase import create_client, Client
from PIL import Image
import pytesseract
from PyPDF2 import PdfReader
import base64
import io
import time

# Initialize clients
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)

supabase = create_client(
    "https://jclnjpqnoxtbvidvwgnx.supabase.co",
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpjbG5qcHFub3h0YnZpZHZ3Z254Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQ1MzA0MjQsImV4cCI6MjA2MDEwNjQyNH0.fxLXrUoogJk3HYlTqvOejvg2Gk4oK9aDQLeU1IOLYNU"
)

# Custom CSS for ChatGPT UI
st.markdown("""
<style>
    /* Main container */
    .main {
        background-color: #f7f7f8;
    }
    
    /* Chat container */
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
        padding-bottom: 100px;
    }
    
    /* Message bubbles */
    .assistant-message {
        background-color: #f7f7f8;
        padding: 12px 16px;
        border-radius: 18px 18px 18px 0;
        margin: 8px 0;
        max-width: 80%;
        word-wrap: break-word;
    }
    
    .user-message {
        background-color: #3b82f6;
        color: white;
        padding: 12px 16px;
        border-radius: 18px 18px 0 18px;
        margin: 8px 0;
        margin-left: auto;
        max-width: 80%;
        word-wrap: break-word;
    }
    
    /* Chat input */
    .chat-input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: white;
        padding: 16px;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
    }
    
    .chat-input-box {
        width: 100%;
        border-radius: 24px;
        padding: 12px 16px;
        border: 1px solid #d9d9e3;
        outline: none;
    }
    
    /* Upload button */
    .upload-btn {
        position: absolute;
        right: 30px;
        bottom: 28px;
        background: none;
        border: none;
        cursor: pointer;
        font-size: 20px;
    }
    
    /* Sidebar */
    .sidebar .sidebar-content {
        background-color: #f7f7f8;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "current_chat" not in st.session_state:
    st.session_state.current_chat = "default"

# Sidebar for chat management
with st.sidebar:
    st.title("Chat History")
    
    # Button to start new chat
    if st.button("+ New Chat"):
        st.session_state.current_chat = f"chat_{int(time.time())}"
        st.session_state.messages = []
    
    # Display chat history (simplified)
    st.write("Previous Chats")
    st.write("- Chat 1")
    st.write("- Chat 2")

# Main chat interface
st.title("ChatGPT Clone")

# Display messages
for message in st.session_state.messages:
    if message["role"] == "assistant":
        st.markdown(f'<div class="assistant-message">{message["content"]}</div>', unsafe_allow_html=True)
    else:
        if message["type"] == "text":
            st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
        elif message["type"] == "image":
            st.image(message["content"], width=300)
            st.markdown('<div class="user-message">[Image]</div>', unsafe_allow_html=True)
        elif message["type"] == "pdf":
            st.markdown('<div class="user-message">[PDF File]</div>', unsafe_allow_html=True)

# Chat input with upload button
input_container = st.container()
with input_container:
    col1, col2 = st.columns([10, 1])
    with col1:
        user_input = st.text_input(
            "Type your message...", 
            key="input",
            label_visibility="collapsed"
        )
    with col2:
        uploaded_file = st.file_uploader(
            "📎", 
            type=["jpg", "jpeg", "png", "pdf"],
            label_visibility="collapsed",
            key="file_uploader"
        )

# Handle text input
if user_input:
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "type": "text"
    })
    
    # Generate response
    response = "This is a simulated response from the AI assistant."
    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "type": "text"
    })
    
    # Rerun to update display
    st.rerun()

# Handle file upload
if uploaded_file:
    if uploaded_file.type.startswith('image'):
        image = Image.open(uploaded_file)
        st.session_state.messages.append({
            "role": "user",
            "content": image,
            "type": "image"
        })
        
        # Simulate image analysis
        response = "I've analyzed this image. It appears to be a nice picture!"
        st.session_state.messages.append({
            "role": "assistant",
            "content": response,
            "type": "text"
        })
        
    elif uploaded_file.type == "application/pdf":
        st.session_state.messages.append({
            "role": "user",
            "content": "PDF file uploaded",
            "type": "pdf"
        })
        
        # Simulate PDF analysis
        response = "I've processed your PDF document. It contains important information."
        st.session_state.messages.append({
            "role": "assistant",
            "content": response,
            "type": "text"
        })
    
    # Rerun to update display
    st.rerun()
