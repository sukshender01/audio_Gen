# app.py
import streamlit as st
from TTS.api import TTS
import soundfile as sf

st.title("Japanese Speech Synthesizer 🎤")
st.write("Enter English text to generate Japanese speech.")

# Text input
text_input = st.text_area("Enter text:", height=150)

if st.button("Generate Speech"):
    if not text_input.strip():
        st.error("Please enter some text.")
    else:
        with st.spinner("Generating speech..."):
            # Load Japanese TTS model
            tts = TTS(model_name="tts_models/ja/kokoro/tacotron2")

            # Generate audio
            audio_file = "japanese_speech.wav"
            tts.tts_to_file(text=text_input, file_path=audio_file)

            # Save transcript
            transcript_file = "transcript.txt"
            with open(transcript_file, "w", encoding="utf-8") as f:
                f.write(text_input)

        st.success("Speech generated successfully ✅")

        # Play audio
        st.audio(audio_file)

        # Download buttons
        st.download_button("Download Audio", data=open(audio_file, "rb").read(), file_name=audio_file, mime="audio/wav")
        st.download_button("Download Transcript", data=open(transcript_file, "r", encoding="utf-8").read(), file_name=transcript_file, mime="text/plain")
