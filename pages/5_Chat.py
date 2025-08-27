import streamlit as st
import requests
import json
if st.sidebar.button("Results"):
    st.switch_page("pages/6_Result.py")
st.sidebar.title("Chat with TalentScout Bot")
st.sidebar.divider()
st.markdown("<h1 style='text-align: center;'>TalentScout Bot</h1>", unsafe_allow_html=True)
API_URL = "https://router.huggingface.co/v1/chat/completions"
try:
    HF_TOKEN=st.secrets["HF_TOKEN"]
except FileNotFoundError:
    st.error("HF_TOKEN secret not found. Please create a .streamlit/secrets.toml file with your Hugging Face token.")
    st.stop()
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def get_response_stream(chat_history):
    payload = {
        "model":"meta-llama/Llama-3.1-8B-Instruct:cerebras",
        "messages":chat_history,
        "stream":True
    }
    try:
        with requests.post(API_URL, headers=headers, json=payload, stream=True) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if not line.startswith(b"data:"):
                    continue
                if line.strip() == b"data: [DONE]":
                    break
                json_data = json.loads(line.decode("utf-8").lstrip("data:").rstrip("/n"))
                if "choices" in json_data and json_data["choices"][0]["delta"].get("content"):
                    yield json_data["choices"][0]["delta"]["content"]
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")
    except json.JSONDecodeError as e:
        st.error(f"Failed to decode JSON from API response: {e}")

if "messages" not in st.session_state:
    st.session_state.messages=[]
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
if prompt := st.chat_input("What would you like to ask?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        full_response = st.write_stream(get_response_stream(st.session_state.messages))
    st.session_state.messages.append({"role": "assistant", "content": full_response})