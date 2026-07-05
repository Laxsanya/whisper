import streamlit as st
import whisper
import tempfile

# ===== PAGE CONFIG =====
st.set_page_config(page_title="Laxsanya Whisper AI", layout="wide")

# ===== YOUR DESIGN (RESTORED EXACTLY) =====
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
    ["tiny", "base"]   # ⚠️ IMPORTANT: removed heavy models to STOP 503
)

show_audio = st.sidebar.checkbox("Show Audio Player", True)

# ===== LOAD MODEL SAFELY =====
@st.cache_resource
def load_model(name):
    return whisper.load_model(name)

# ===== UPLOAD =====
uploaded_file = st.file_uploader(
    "Upload Audio File (.mp3, .wav, .m4a)",
    type=["mp3", "wav", "m4a"]
)

if uploaded_file is not None:

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp.write(uploaded_file.read())
        audio_path = tmp.name

    if show_audio:
        st.audio(audio_path)

    try:
        with st.spinner("Loading model..."):
            model = load_model(model_size)

        with st.spinner("Transcribing audio..."):
            result = model.transcribe(audio_path)

        st.success("Transcription Completed!")

        st.subheader("Transcribed Text")
        st.text_area("", result["text"], height=300)

    except Exception as e:
        st.error("Something went wrong. Please try again.")
        st.error(str(e))

# ===== FOOTER =====
st.markdown("""
<p style='text-align: center; color: #FF4B4B;'>
Developed by Laxsanya RJ
</p>
""", unsafe_allow_html=True)
