import streamlit as st
import requests , os
from dotenv import load_dotenv


load_dotenv()
st.header("Learning End to end bot Deployment with API")


API_URL = os.getenv("API_URL")


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Streamed response emulator    
def stream_llm_response(user_input):
    full_url = f"{API_URL}/chat/{user_input}"
    response = requests.post(full_url)
    return response.text
            

user_input = st.chat_input(placeholder="Write your query")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role":"user","content":user_input})

    with st.chat_message("assistant"):

        response = stream_llm_response(user_input)
        st.write(response)
        
    st.session_state.messages.append({"role":"assistant","content":response})
    