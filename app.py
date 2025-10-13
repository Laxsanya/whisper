# Laxsanya Whisper AI - Vibrant Streamlit Web App

import streamlit as st
import whisper
import tempfile
from pathlib import Path

# Page configuration
st.set_page_config(page_title="Laxsanya Whisper AI", layout="wide")
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>Laxsanya Whisper AI - Speech-to-Text</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #FFB347;'>Upload your audio and get instant AI-powered transcription!</p>", unsafe_allow_html=True)

# Sidebar options
st.sidebar.header("Settings")
model_size = st.sidebar.selectbox("Choose Whisper Model", ["tiny", "base", "small", "medium", "large"])
show_audio_waveform = st.sidebar.checkbox("Show Audio Waveform", value=True)

# File uploader
uploaded_file = st.file_uploader("Upload Audio File (.mp3, .wav, .m4a)", type=["mp3", "wav", "m4a"])

if uploaded_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    st.audio(tfile.name)

    try:
        with st.spinner(f"Loading {model_size} Whisper model..."):
            model = whisper.load_model("tiny")
        with st.spinner("Transcribing audio..."):
            result = model.transcribe(tfile.name)
        st.success("Transcription Completed!")

        st.subheader("Transcribed Text")
        st.text_area("Your Transcription", result['text'], height=300)

        if show_audio_waveform:
            st.audio(tfile.name)
            st.markdown("<p style='color: #4B88FF;'>Waveform visualization will be here in full version.</p>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error: {e}")

st.markdown("<p style='text-align: center; color: #FF4B4B;'>Developed by Laxsanya RJ</p>", unsafe_allow_html=True)
