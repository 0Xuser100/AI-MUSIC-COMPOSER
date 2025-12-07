import streamlit as st
from main import MusicLLM
from utils import *
from io import BytesIO
from logging_setup import setup_logger
from dotenv import load_dotenv
import base64

logger = setup_logger()
load_dotenv()


# ---------------------------
# Load Background Image
# ---------------------------
def set_background(image_path):
    with open(image_path, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
        }}
        /* Center container */
        .main > div {{
            max-width: 900px;
            margin: auto;
            background: rgba(0,0,0,0.35);
            padding: 20px;
            border-radius: 15px;
        }}
        /* Title */
        h1 {{
            color: #ffffff !important;
            text-align: center;
            text-shadow: 0px 0px 10px #000;
        }}
        /* Text */
        .stMarkdown, p, label {{
            color: #f3f3f3 !important;
            font-size: 16px;
        }}
        /* Input box */
        .stTextInput > div > div > input {{
            border-radius: 10px;
            padding: 10px;
        }}
        /* Dropdown */
        .stSelectbox > div > div {{
            border-radius: 10px !important;
        }}
        /* Button styling */
        .stButton>button {{
            background-color: #6c63ff;
            color: white;
            padding: 0.7rem 1.4rem;
            border-radius: 10px;
            border: none;
            font-weight: 600;
            transition: 0.3s;
        }}
        .stButton>button:hover {{
            background-color: #4b45d1;
            color: #fff;
        }}
        /* Expander */
        .streamlit-expanderHeader {{
            color: white !important;
            font-size: 18px;
            font-weight: bold;
        }}
        </style>
    """,
        unsafe_allow_html=True,
    )


# Apply background
set_background("background.jfif")

# ---------------------------
# Streamlit App
# ---------------------------

st.set_page_config(page_title="AI Music Composer", layout="centered")

st.markdown(
    """
    <h1>🎵 AI Music Composer</h1>
    <p style="text-align:center; color:#eee; font-size:18px;">
        Describe your idea — and let AI transform it into music.
    </p>
    """,
    unsafe_allow_html=True,
)

# Info card
st.markdown(
    """
    <div style="
        background: rgba(0,0,0,0.5);
        padding: 15px;
        border-radius: 10px;
        border:1px solid #ffffff25;
        margin-bottom:20px;
        color:white;">
        <b>How it works:</b><br>
        1. Describe a melody idea<br>
        2. Choose a style<br>
        3. AI composes melody, harmony & rhythm<br>
        4. Listen instantly 🎧
    </div>
    """,
    unsafe_allow_html=True,
)

# Inputs
music_input = st.text_input("🎼 Describe the music you want to compose")
style = st.selectbox(
    "🎚️ Choose a style", ["Sad", "Happy", "Jazz", "Romantic", "Extreme"]
)

# Generate button
if st.button("🎶 Generate Music") and music_input:
    generator = MusicLLM()
    with st.spinner("🎧 Creating your music, please wait..."):
        melody = generator.generate_melody(music_input)
        harmony = generator.generate_harmony(melody)
        rhythm = generator.generate_rhythm(melody)
        composition = generator.adapt_style(style, melody, harmony, rhythm)

        melody_notes = melody.split()
        melody_freqs = note_to_frequencies(melody_notes)

        harmony_chords = harmony.split()
        harmony_notes = []
        for chord in harmony_chords:
            harmony_notes.extend(chord.split("-"))

        harmony_freqs = note_to_frequencies(harmony_notes)

        all_freqs = melody_freqs + harmony_freqs
        wav_bytes = generate_wav_bytes_from_notes_freq(all_freqs)

    # Output card
    st.markdown(
        """
        <div style="
            background: rgba(0,0,0,0.55);
            padding:20px;
            border-radius:15px;
            border:1px solid #ffffff20;">
        """,
        unsafe_allow_html=True,
    )

    st.audio(BytesIO(wav_bytes), format="audio/wav")
    st.success("🎉 Music generated successfully!")

    st.markdown("</div>", unsafe_allow_html=True)

    with st.expander("📄 Composition Summary"):
        st.markdown(
            f"""
        <pre style="color: white; white-space: pre-wrap;">
        {composition}
        </pre>
        """,
            unsafe_allow_html=True,
        )
