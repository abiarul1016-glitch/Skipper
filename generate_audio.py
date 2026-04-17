"""Voice synthesis module using Qwen TTS with voice cloning.

Generates speech audio from text using a reference audio sample to clone
the speaker's voice. Uses MLX Audio library for efficient inference.
"""

import numpy as np
import scipy.io.wavfile as wavfile
from mlx_audio.tts.utils import load_model

from config import Config


def main():
    """Test voice generation with a sample output file."""
    generate_audio(output_file=str(Config.OUTPUT_FILE_DIRECTORY / "test.wav"))


def generate_audio(
    reference_audio=None,
    reference_audio_transcript=None,
    output_file=None,
    text_to_generate="Hey there, how are you?",
    tts_model=None,
):
    """Generate speech audio from text using voice cloning.

    Uses a reference audio sample and its transcript to clone the speaker's voice
    and synthesize new text with that voice.

    Args:
        reference_audio: Path to reference audio file (uses Config default if None)
        reference_audio_transcript: Path to reference transcript (uses Config default if None)
        output_file: Path to save output WAV file (uses Config default if None)
        text_to_generate: Text to synthesize
        tts_model: Qwen TTS model identifier (uses Config default if None)
    """
    # Use Config defaults if not provided
    if reference_audio is None:
        reference_audio = str(Config.REF_AUDIO_PATH)
    if reference_audio_transcript is None:
        reference_audio_transcript = str(Config.REF_AUDIO_TRANSCRIPT)
    if output_file is None:
        output_file = str(Config.OUTPUT_FILE_DIRECTORY / "output.wav")
    if tts_model is None:
        tts_model = Config.TTS_MODEL

    # Read reference transcript
    with open(reference_audio_transcript, "r") as file:
        reference_text = file.read()

    print("🔮 Generating audio...\n")

    # Load TTS model and generate speech
    model = load_model(tts_model)
    results = list(
        model.generate(
            text=text_to_generate, ref_audio=reference_audio, ref_text=reference_text
        )
    )

    # Extract audio data from model output
    audio = results[0].audio

    print("\n✨ Synthesis complete!\n")
    print("Saving to file...")

    # Save audio to file
    audio_data = np.array(audio)
    sample_rate = 24000

    wavfile.write(output_file, sample_rate, audio_data)

    print(f"✅ Saved to: {output_file}!")


if __name__ == "__main__":
    main()
