import requests
import streamlit as st

def get_openai_response(input_text):
    try:
        response = requests.post(
            "http://localhost:8000/essay/invoke",
            json={'input': {'topic': input_text}}
        )
        # Check if the server actually sent a successful response
        if response.status_code == 200:
            return response.json()['output']
        else:
            return f"Server Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"Connection Error: {e}"

def get_ollama_response(input_text):
    try:
        response = requests.post(
            "http://localhost:8000/poem/invoke",
            json={'input': {'topic': input_text}}
        )
        if response.status_code == 200:
            # Logic: Ollama returns a direct string in 'output'
            return response.json()['output']
        else:
            return f"Ollama Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"Connection Error: {e}"

# streamlit framework
st.title('Langchain Demo With LLAMA2 API')
input_text = st.text_input("Write an essay on")
input_text1 = st.text_input("Write a poem on")

if input_text:
    st.write(get_openai_response(input_text))

if input_text1:
    st.write(get_ollama_response(input_text1))