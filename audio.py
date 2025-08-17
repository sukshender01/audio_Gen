# app.py
import streamlit as st
from transformers import pipeline
import numpy as np
from scipy.io.wavfile import write

st.title("Japanese Speech Synthesizer 🎤")
st.write("Enter Japanese text to generate speech.")

text_input = st.text_area("Enter Japanese Text:", height=150)

if st.button("Generate Speech"):
    if not text_input.strip():
        st.error("Please enter some text.")
    else:
        with st.spinner("Generating speech..."):
            # Load the Japanese TTS pipeline
            tts = pipeline("text-to-speech", model="espnet/kan-bayashi_jsut_tts_train_fastspeech_raw_phn_jaconv_pyopenjtalk_train.loss.best")

            # Generate audio
            audio_array, sampling_rate = tts(text_input)

            # Convert float32 [-1,1] to int16 for WAV
            audio_int16 = np.int16(audio_array * 32767)

            # Save audio
            audio_file = "japanese_speech.wav"
            write(audio_file, sampling_rate, audio_int16)

            # Save transcript
            transcript_file = "transcript.txt"
            with open(transcript_file, "w", encoding="utf-8") as f:
                f.write(text_input)

        st.success("Speech generated successfully ✅")

        # Audio player
        st.audio(audio_file, format="audio/wav")

        # Download buttons
        st.download_button("Download Audio", data=open(audio_file, "rb").read(), file_name=audio_file, mime="audio/wav")
        st.download_button("Download Transcript", data=open(transcript_file, "r", encoding="utf-8").read(), file_name=transcript_file, mime="text/plain")
