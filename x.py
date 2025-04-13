import streamlit as st
from openai import OpenAI
from supabase import create_client, Client
from PIL import Image
import pytesseract
from PyPDF2 import PdfReader

# Initialize OpenAI client
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)

# Initialize Supabase client
url = "https://jclnjpqnoxtbvidvwgnx.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpjbG5qcHFub3h0YnZpZHZ3Z254Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQ1MzA0MjQsImV4cCI6MjA2MDEwNjQyNH0.fxLXrUoogJk3HYlTqvOejvg2Gk4oK9aDQLeU1IOLYNU"
supabase: Client = create_client(url, key)

# Function to get JDGPT response
def get_jdgpt_response(messages):
    completion = client.chat.completions.create(
        model="nvidia/llama-3.1-nemotron-ultra-253b-v1",
        messages=messages,
        temperature=0.6,
        top_p=0.95,
        max_tokens=4096,
        frequency_penalty=0,
        presence_penalty=0,
        stream=True
    )

    response = ""
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            response += chunk.choices[0].delta.content
    return response

# Function to save user memory in Supabase
def save_user_memory(user_id, chat_history):
    supabase.table('user_memory').insert({
        'user_id': user_id,
        'chat_history': chat_history
    }).execute()

# Function to analyze images
def analyze_image(image):
    text = pytesseract.image_to_string(image)
    return text

# Function to analyze PDFs
def analyze_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Streamlit UI
st.title("JDGPT - The No-Nonsense Chatbot")
st.write("Get ready for some brutal honesty. No fluff, just truth.")

user_id = st.text_input("Enter your user ID:", value="unique_user_id")

# Chat input
user_input = st.text_input("You:", key="user_input")

if st.session_state.get("user_input"):
    # Get JDGPT response
    response = get_jdgpt_response([{"role": "user", "content": st.session_state.user_input}])
    
    # Display the response
    st.write("**JDGPT:**", response)
    
    # Save chat history
    save_user_memory(user_id, st.session_state.user_input + "\n" + response)

    # Clear the input after processing
    st.session_state.user_input = ""

# Image upload
uploaded_image = st.file_uploader("Upload an image for analysis", type=["jpg", "jpeg", "png"])
if uploaded_image is not None:
    image = Image.open(uploaded_image)
    image_text = analyze_image(image)
    st.write("**Image Analysis:**", image_text)

# PDF upload
uploaded_pdf = st.file_uploader("Upload a PDF for analysis", type=["pdf"])
if uploaded_pdf is not None:
    pdf_text = analyze_pdf(uploaded_pdf)
    st.write("**PDF Analysis:**", pdf_text)

# Error handling
try:
    # Your main code logic here
    pass
except Exception as e:
    st.error(f"An error occurred: {e}")
