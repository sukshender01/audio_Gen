# app.py
import streamlit as st
import os
import soundfile as sf

# Try importing TTS; provide clear error if not installed
try:
    from TTS.api import TTS
except ImportError:
    st.error("TTS library is not installed. Add 'TTS' to requirements.txt.")
    st.stop()

# ----------------------------
# Streamlit UI
# ----------------------------
st.title("English to Japanese Speech Synthesizer 🎤")
st.write("Enter English text below and generate Japanese speech with downloadable files.")

# Text input
english_text = st.text_area("Enter English Text:", height=150)

# Generate speech on button click
if st.button("Generate Japanese Speech"):
    if not english_text.strip():
        st.error("Please enter some text to generate speech.")
    else:
        with st.spinner("Generating Japanese speech..."):
            # Initialize TTS model
            # Use a multilingual or Japanese TTS model available in TTS library
            tts_model_name = "tts_models/multilingual/multi-dataset/tacotron2-DDC"  
            tts = TTS(tts_model_name)

            # Output audio file
            audio_file = "japanese_speech.wav"
            tts.tts_to_file(text=english_text, file_path=audio_file, language="ja")

            # Save transcript
            transcript_file = "transcript.txt"
            with open(transcript_file, "w", encoding="utf-8") as f:
                f.write(english_text)

        st.success("Japanese speech generated successfully! ✅")

        # Show audio player
        st.audio(audio_file, format="audio/wav")

        # Download buttons
        st.download_button(
            label="Download Audio File",
            data=open(audio_file, "rb").read(),
            file_name=audio_file,
            mime="audio/wav"
        )

        st.download_button(
            label="Download Transcript",
            data=open(transcript_file, "r", encoding="utf-8").read(),
            file_name=transcript_file,
            mime="text/plain"
        )

        # Optional: Clean up after download
        # os.remove(audio_file)
        # os.remove(transcript_file)
