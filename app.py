import streamlit as st
import whisper
import tempfile

st.set_page_config(page_title="Laxsanya Whisper AI", layout="wide")

st.title("Laxsanya Whisper AI - Speech-to-Text")

# Sidebar
model_size = st.sidebar.selectbox("Choose Whisper Model", ["tiny", "base", "small"])

uploaded_file = st.file_uploader("Upload Audio File (.mp3, .wav, .m4a)", type=["mp3", "wav", "m4a"])

# ✅ IMPORTANT: cache model properly (DO NOT LOAD ON PAGE START)
@st.cache_resource
def load_model(name):
    return whisper.load_model(name)

# 👇 DO NOT load model here
# model = load_model(model_size) ❌ REMOVE THIS

if uploaded_file is not None:

    # Load model ONLY when needed
    with st.spinner("Loading model... (first time only)"):
        model = load_model(model_size)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp.write(uploaded_file.read())
        audio_path = tmp.name

    st.audio(audio_path)

    with st.spinner("Transcribing audio..."):
        result = model.transcribe(audio_path)

    st.success("Done!")

    st.text_area("Transcription", result["text"], height=300)
