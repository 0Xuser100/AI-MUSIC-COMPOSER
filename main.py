"""MusicLLM demo entrypoint for Groq-powered music generation."""

import os

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from logging_setup import setup_logger

logger = setup_logger()

load_dotenv()
api_key = os.getenv("GROQ_API_KEY", "").strip()
if not api_key:
    raise ValueError("Missing GROQ_API_KEY. Set it as an env var or pass api_key=...")

MELODY_PROMPT = ChatPromptTemplate.from_template(
    "Generate a melody based on this input: {input}. Represent it as a space seperated notes (eg., C4 D4 E4)"
)
HARMONY_PROMPT = ChatPromptTemplate.from_template(
    "Create harmony chords for this melody: {melody}. Format: C4-E4-G4 F4-A4-C5"
)
RHYTHM_PROMPT = ChatPromptTemplate.from_template(
    "Suggest rhythm durations (in beats) for this melody: {melody}. Format: 1.0 0.5 0.5 2.0"
)
STYLE_PROMPT = ChatPromptTemplate.from_template(
    "Adapt to {style} style: \n Melody: {melody}\nHarmony: {harmony}\n Rhythm: {rhythm}\nOutput single string summary"
)


class MusicLLM:
    """High-level helper that wraps Groq's chat API for music generation tasks."""

    def __init__(self, temperature: float = 0.7) -> None:
        """Create a Groq-backed LLM instance configured for music prompts.

        Args:
            temperature: Sampling temperature forwarded to the Groq chat model.
        """

        self.llm = ChatGroq(
            temperature=temperature,
            groq_api_key=api_key,
            model_name="llama-3.1-8b-instant",
        )

    def generate_melody(self, user_input: str) -> str:
        """Generate a space-separated note sequence from a free-text prompt."""

        chain = MELODY_PROMPT | self.llm
        return chain.invoke({"input": user_input}).content.strip()

    def generate_harmony(self, melody: str) -> str:
        """Create supporting harmony chords for a given melody string."""

        chain = HARMONY_PROMPT | self.llm
        return chain.invoke({"melody": melody}).content.strip()

    def generate_rhythm(self, melody: str) -> str:
        """Suggest rhythm durations that match the provided melody notes."""

        chain = RHYTHM_PROMPT | self.llm
        return chain.invoke({"melody": melody}).content.strip()

    def adapt_style(self, style: str, melody: str, harmony: str, rhythm: str) -> str:
        """Summarize the composition in a target style using melody, harmony, and rhythm."""

        chain = STYLE_PROMPT | self.llm
        return chain.invoke(
            {"style": style, "melody": melody, "harmony": harmony, "rhythm": rhythm}
        ).content.strip()


if __name__ == "__main__":
    music = MusicLLM(temperature=0.7)

    idea = "happy upbeat pop melody"
    logger.info("Starting composition for idea '{}'", idea)
    melody = music.generate_melody(idea)
    harmony = music.generate_harmony(melody)
    rhythm = music.generate_rhythm(melody)
    styled = music.adapt_style("jazz", melody, harmony, rhythm)

    logger.info("Melody: {}", melody)
    logger.info("Harmony: {}", harmony)
    logger.info("Rhythm: {}", rhythm)
    logger.info("Styled: {}", styled)
