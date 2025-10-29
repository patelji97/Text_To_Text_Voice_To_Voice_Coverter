import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import sounddevice as sd
import wavio
from pydub import AudioSegment
from scipy.io import wavfile
import tempfile
import os

# ==========================
# 🎧 FUNCTIONS
# ==========================

# Record voice using sounddevice
def record_audio(duration=5, fs=16000):
    st.info(f"🎙 Recording for {duration} seconds...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp:
        wavio.write(temp.name, recording, fs, sampwidth=2)
        return temp.name

# Speech → Text
def speech_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio, language="en-IN")
        return text
    except sr.UnknownValueError:
        return " Could not understand the audio."
    except sr.RequestError:
        return " Network error. Please check your internet."

# Text Converter
def text_converter(text, mode):
    if mode == "UPPER":
        return text.upper()
    elif mode == "lower":
        return text.lower()
    elif mode == "reverse":
        return text[::-1]
    else:
        return text

# Text → Speech
def text_to_speech(text):
    tts = gTTS(text=text, lang="en")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp:
        tts.save(temp.name)
        return temp.name


#  🎛 STREAMLIT UI

st.set_page_config(page_title="Text ↔ Voice Converter", page_icon="🎙", layout="centered")

st.title(" Voice ↔ Voice & Text ↔ Text Converter")
st.caption("Convert your **voice or text**")

option = st.sidebar.radio("Choose Conversion Type", ["Text → Text", "Voice → Voice"])

# --------------------------
#  TEXT → TEXT SECTION
# --------------------------
if option == "Text → Text":
    st.header(" Text to Text Converter")
    text = st.text_area(" Enter your text:")
    mode = st.selectbox(" Choose conversion mode:", ["UPPER", "lower", "reverse"])

    if st.button("Convert Text"):
        if text.strip():
            converted = text_converter(text, mode)
            st.success(" Converted Text:")
            st.code(converted)
        else:
            st.warning(" Please enter some text to convert.")

# --------------------------
#  VOICE → VOICE SECTION
# --------------------------
elif option == "Voice → Voice":
    st.header(" Voice to Voice Converter")
    duration = st.slider("🎚 Recording Duration (seconds)", 3, 10, 5)

    if st.button(" Start Recording"):
        try:
            filename = record_audio(duration)
            st.success(" Recording complete!")

            text = speech_to_text(filename)
            st.write(" You said:", text)

            converted_text = text_converter(text, "UPPER")
            st.write( "Converted Text:", converted_text)

            if converted_text:
                audio_file = text_to_speech(converted_text)
                st.audio(audio_file, format="audio/mp3")
                st.download_button(
                    label=" Download Converted Voice",
                    data=open(audio_file, "rb").read(),
                    file_name="converted_voice.mp3",
                    mime="audio/mp3"
                )
        except Exception as e:
            st.error(f"Error: {e}")



st.markdown(" *Developed by Disha — Made simple for  interview demo!* ")
