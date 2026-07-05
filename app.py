import streamlit as st
import whisper
import tempfile
import os

# ===== PAGE CONFIG =====
st.set_page_config(page_title="Laxsanya Whisper AI", layout="wide")

# ===== UI (UNCHANGED) =====
st.markdown("""
<h1 style='text-align: center; color: #FF4B4B;'>
Laxsanya Whisper AI - Speech-to-Text
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<p style='text-align: center; color: #FFB347;'>
Upload your audio and get instant AI-powered transcription!
</p>
""", unsafe_allow_html=True)

# ===== SIDEBAR =====
st.sidebar.header("Settings")

model_size = st.sidebar.selectbox(
    "Choose Whisper Model",
    ["tiny", "base"]
)

show_audio = st.sidebar.checkbox("Show Audio Player", True)

# ===== LOAD MODEL (FIXED CACHE) =====
@st.cache_resource
def load_model(name):
    return whisper.load_model(name)

model = load_model(model_size)

# ===== UPLOAD =====
uploaded_file = st.file_uploader(
    "Upload Audio File (.mp3, .wav, .m4a)",
    type=["mp3", "wav", "m4a"]
)

if uploaded_file is not None:

    file_ext = uploaded_file.name.split(".")[-1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_ext}") as tmp:
        tmp.write(uploaded_file.read())
        audio_path = tmp.name

    if show_audio:
        st.audio(audio_path)

    try:
        with st.spinner("Transcribing audio..."):
            result = model.transcribe(audio_path)

        text = result.get("text", "")

        st.success("Transcription Completed!")

        st.subheader("Transcribed Text")
        st.text_area("", text, height=300)

        if text.strip() == "":
            st.warning("No speech detected in audio.")

    except Exception as e:
        st.error("Something went wrong during transcription.")
        st.error(str(e))

    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)

# ===== FOOTER =====
st.markdown("""
<p style='text-align: center; color: #FF4B4B;'>
Developed by Laxsanya RJ
</p>
""", unsafe_allow_html=True)
