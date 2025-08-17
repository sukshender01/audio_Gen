# app.py
import streamlit as st
from transformers import pipeline

st.title("English to Japanese Speech Synthesizer 🎤")
st.write("Enter English text below to generate Japanese speech with downloadable files.")

text_input = st.text_area("Enter English Text:", height=150)

if st.button("Generate Japanese Speech"):
    if not text_input.strip():
        st.error("Please enter some text to generate speech.")
    else:
        with st.spinner("Generating Japanese speech..."):
            # Load Hugging Face TTS pipeline (multilingual)
            tts = pipeline("text-to-speech", model="espnet/kan-bayashi_ljspeech_tts_train")

            # Generate audio
            audio_array, sampling_rate = tts(text_input)

            # Save audio
            audio_file = "japanese_speech.wav"
            from scipy.io.wavfile import write
            write(audio_file, sampling_rate, audio_array)

            # Save transcript
            transcript_file = "transcript.txt"
            with open(transcript_file, "w", encoding="utf-8") as f:
                f.write(text_input)

        st.success("Japanese speech generated successfully! ✅")

        st.audio(audio_file, format="audio/wav")
        st.download_button("Download Audio", data=open(audio_file, "rb").read(), file_name=audio_file, mime="audio/wav")
        st.download_button("Download Transcript", data=open(transcript_file, "r", encoding="utf-8").read(), file_name=transcript_file, mime="text/plain")
