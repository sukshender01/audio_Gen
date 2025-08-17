# streamlit_app.py
import streamlit as st
import requests
from io import BytesIO
import base64

st.title("Text-to-Speech with Hugging Face API")

# Input text
text = st.text_area("Enter text to convert to speech:")

# Model selection
model_id = "espnet/kan-bayashi_ljspeech_tts_train"  # public model on Hugging Face

# Hugging Face API token
HF_API_TOKEN = st.secrets.get("HF_API_TOKEN")  # Add your token in Streamlit secrets

def tts_hf(text, model_id, token):
    headers = {"Authorization": f"Bearer {token}"}
    API_URL = f"https://api-inference.huggingface.co/models/{model_id}"
    payload = {"inputs": text}

    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        st.error(f"Error from Hugging Face API: {response.status_code}")
        return None

    return BytesIO(response.content)  # returns audio file

if st.button("Generate Speech"):
    if not text.strip():
        st.warning("Please enter some text!")
    elif not HF_API_TOKEN:
        st.error("Hugging Face API token is missing! Add it to Streamlit secrets.")
    else:
        audio_bytes = tts_hf(text, model_id, HF_API_TOKEN)
        if audio_bytes:
            st.audio(audio_bytes, format="audio/wav")
            st.success("Speech generated successfully!")
