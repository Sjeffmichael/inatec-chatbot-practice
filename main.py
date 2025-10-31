# frontend.py

import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Define the URL of the Flask backend
API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = os.getenv("API_KEY")

st.title("⚽ Chatbot Experto en Futbol")

# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display prior chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input from the chat input box
if prompt := st.chat_input("Haz cualquier consulta sobre futbot"):
    # Add user message to the chat history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Send the user's message to the Flask backend
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "system", "content": "Hablame exclusivamente de futbol lo demás no te puedo dar respuesta."}, 
                {"role": "user", "content": prompt}
            ]
        }
        response = requests.post(API_URL, headers=headers, data=json.dumps(data))
    
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        
        # Get the bot's response from the backend
        bot_response = response.json()['choices'][0]['message']['content']

        # Display the bot's response and add it to chat history
        with st.chat_message("assistant"):
            st.markdown(bot_response)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})

    except requests.exceptions.RequestException as e:
        st.error(f"Could not connect to the backend: {e}")