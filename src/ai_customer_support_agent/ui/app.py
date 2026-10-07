import os
import uuid

import requests
import streamlit as st
from dotenv import load_dotenv


load_dotenv()

API_URL = "http://127.0.0.1:8000/chat"
API_KEY = os.getenv("CUSTOMER_002_API_KEY")




st.set_page_config(
    page_title="AI Customer Support",
    page_icon="🤖",
)

st.title("🤖 AI Customer Support")
st.write(
    "Ask about your orders, company policies, products, "
    "or create a support ticket."
)
if st.button("New Chat"):
    st.session_state.messages = []
    st.session_state.thread_id = str(uuid.uuid4())
    st.rerun()
    

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


user_message = st.chat_input("Type your message...")

if user_message:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message,
        }
    )

    with st.chat_message("user"):
        st.write(user_message)

    try:
        response = requests.post(
            API_URL,
            headers={
                "X-API-Key": API_KEY,
            },
            json={
                "message": user_message,
                "thread_id": st.session_state.thread_id,
            },
            timeout=60,
        )

        response.raise_for_status()

        assistant_message = response.json()["response"]

    except requests.RequestException:
        assistant_message = (
            "Sorry, I couldn't connect to the support service."
        )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_message,
        }
    )

    with st.chat_message("assistant"):
        st.write(assistant_message)