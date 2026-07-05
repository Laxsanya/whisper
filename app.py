# Laxsanya Whisper AI - Vibrant Streamlit Web App

import streamlit as st
import whisper
import tempfile

# Page configuration
st.set_page_config(page_title="Laxsanya Whisper AI", layout="wide")

st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>Laxsanya Whisper AI - Speech-to-Text</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #FFB347;'>Upload your audio and get instant AI-powered transcription!</p>", unsafe_allow_html=True)

# Sidebar options
st.sidebar.header("Settings")
model_size = st.sidebar.selectbox("Choose Whisper Model", ["tiny", "base", "small", "medium", "large"])
show_audio = st.sidebar.checkbox("Show Audio Player", value=True)

# Cache model so it doesn't reload every time
@st.cache_resource
def load_model(name):
    return whisper.load_model(name)

uploaded_file = st.file_uploader("Upload Audio File (.mp3, .wav, .m4a)", type=["mp3", "wav", "m4a"])

if uploaded_file is not None:

    # Save temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp.write(uploaded_file.read())
        audio_path = tmp.name

    if show_audio:
        st.audio(audio_path)

    try:
        # Load selected model
        with st.spinner(f"Loading {model_size} model..."):
            model = load_model(model_size)

        # Transcribe
        with st.spinner("Transcribing audio..."):
            result = model.transcribe(audio_path)

        # OUTPUT
        st.success("Transcription Completed!")

        st.subheader("Transcribed Text")
        st.text_area("Your Transcription", result["text"], height=300)

    except Exception as e:
        st.error(f"Error: {e}")

st.markdown("<p style='text-align: center; color: #FF4B4B;'>Developed by Laxsanya RJ</p>", unsafe_allow_html=True)
