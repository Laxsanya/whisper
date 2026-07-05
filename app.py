# Laxsanya Whisper AI - Vibrant Streamlit Web App

import streamlit as st
import whisper
import tempfile

# Page configuration
st.set_page_config(page_title="Laxsanya Whisper AI", layout="wide")

# ===== YOUR DESIGN (UNCHANGED) =====
st.markdown(
    "<h1 style='text-align: center; color: #FF4B4B;'>Laxsanya Whisper AI - Speech-to-Text</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center; color: #FFB347;'>Upload your audio and get instant AI-powered transcription!</p>",
    unsafe_allow_html=True
)

# ===== SIDEBAR (UNCHANGED) =====
st.sidebar.header("Settings")

model_size = st.sidebar.selectbox(
    "Choose Whisper Model",
    ["tiny", "base", "small", "medium", "large"]
)

show_audio_waveform = st.sidebar.checkbox("Show Audio Waveform", value=True)

# ===== FIX: LOAD MODEL PROPERLY (NO FREEZING) =====
@st.cache_resource
def load_model(name):
    return whisper.load_model(name)

# ===== FILE UPLOADER =====
uploaded_file = st.file_uploader(
    "Upload Audio File (.mp3, .wav, .m4a)",
    type=["mp3", "wav", "m4a"]
)

# ===== MAIN LOGIC =====
if uploaded_file is not None:

    # Save uploaded file properly
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp.write(uploaded_file.read())
        audio_path = tmp.name

    # Show audio player
    st.audio(audio_path)

    try:
        # Load model ONLY when needed
        with st.spinner(f"Loading {model_size} model..."):
            model = load_model(model_size)

        # Transcription
        with st.spinner("Transcribing audio... please wait"):
            result = model.transcribe(audio_path)

        # Success output
        st.success("Transcription Completed!")

        # Show text
        st.subheader("Transcribed Text")
        st.text_area("Your Transcription", result["text"], height=300)

        # Optional waveform placeholder
        if show_audio_waveform:
            st.markdown(
                "<p style='color:#4B88FF;'>Waveform visualization will be here in full version.</p>",
                unsafe_allow_html=True
            )

    except Exception as e:
        st.error(f"Something went wrong: {e}")

# ===== FOOTER (UNCHANGED) =====
st.markdown(
    "<p style='text-align: center; color: #FF4B4B;'>Developed by Laxsanya RJ</p>",
    unsafe_allow_html=True
)
