import streamlit as st
from dotenv import load_dotenv
import os
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.getenv("API_KEY"));
st.set_page_config(page_title="AI Chatbot", page_icon=":shark:", layout="centered")


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("AI Chatbot")


for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


user_prompt = st.chat_input("Type your message here...")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)

    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # Format the chat history for the API
    formatted_history = []
    for msg in st.session_state.chat_history:
        role = "user" if msg["role"] == "user" else "model" # Map 'system' role to 'model'
        formatted_history.append(types.Content(role=role, parts=[types.Part(text=msg["content"])]))

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        config=types.GenerateContentConfig(
            system_instruction="You are a helpful assistant that can answer questions and help with tasks.",
        ),
        contents=formatted_history # Use the formatted history directly
    )

    st.session_state.chat_history.append({"role": "system", "content": response.text})

    with st.chat_message("system"):
        st.markdown(response.text)

        
        





    

