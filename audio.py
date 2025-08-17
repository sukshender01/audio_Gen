# app.py
import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForSpeechSeq2Seq
import soundfile as sf
import os

# ----------------------------
# Setup
# ----------------------------
st.title("English to Japanese Speech Synthesizer 🎤")
st.write("Enter English text below, and generate Japanese speech with downloadable files.")

# Text input
english_text = st.text_area("Enter English Text:", height=150)

# Button to trigger conversion
if st.button("Generate Japanese Speech"):
    if not english_text.strip():
        st.error("Please enter some text to generate speech.")
    else:
        with st.spinner("Generating Japanese speech..."):
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            
            # Load model & tokenizer
            model_name = "fish-audio/fish-speech-1-japanese"
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForSpeechSeq2Seq.from_pretrained(model_name).to(device)
            
            # Tokenize input
            inputs = tokenizer(english_text, return_tensors="pt").to(device)
            
            # Generate speech
            with torch.no_grad():
                speech = model.generate(**inputs)
            
            # Convert to numpy array
            speech_audio = speech.squeeze().cpu().numpy()
            
            # Save audio file
            audio_file = "japanese_speech.wav"
            sf.write(audio_file, speech_audio, samplerate=22050)
            
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
        
        # Optional: Clean up files after download
        # os.remove(audio_file)
        # os.remove(transcript_file)
