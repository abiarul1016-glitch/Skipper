"""Centralized configuration management for Skipper.

Loads environment variables from secrets.env and provides a single source of truth
for all configuration values. Validates required variables on import to fail fast.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from secrets file
SECRETS_FILE_PATH = "/Users/abishanarulselvan/CODING/Skipper/secrets.env"
load_dotenv(SECRETS_FILE_PATH)


class Config:
    """Centralized configuration with validation."""

    # Paths
    PROJECT_ROOT = Path(__file__).parent
    OUTPUT_FILE_DIRECTORY = PROJECT_ROOT / "output_audios"
    REF_AUDIO_PATH = PROJECT_ROOT / "reference_audios" / "appa_reference.wav"
    REF_AUDIO_TRANSCRIPT = PROJECT_ROOT / "reference_audios" / "appa_reference.txt"

    # External Services
    NGROK_URL = os.getenv("NGROK_URL", "https://incubous-caitlyn-herby.ngrok-free.dev")

    # Twilio
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    MY_PHONE_NUMBER = os.getenv("MY_PHONE_NUMBER")
    TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

    # Phone Numbers
    DAD_PHONE_NUMBER = os.getenv("DAD_PHONE_NUMBER")
    SCHOOL_PHONE_NUMBER = os.getenv("SCHOOL_PHONE_NUMBER")

    # LLM Models
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3.5")
    TTS_MODEL = os.getenv("TTS_MODEL", "mlx-community/Qwen3-TTS-12Hz-1.7B-Base-bf16")

    # Calendar
    SKIP_CALENDAR_ID = os.getenv("SKIP_CALENDAR_ID")

    # Call Configuration
    SEND_DIGITS = "WWWWWWW1"
    PAUSE_SECONDS = 20  # Wait past second recording instruction

    # Service Startup
    FLASK_PORT = 8000
    SERVICE_START_TIMEOUT = 10  # seconds to wait for services to start

    # Recording
    RECORDING = os.getenv("RECORDING", "False") == "True"

    # Call Routing (can be overridden)
    FROM_NUMBER = DAD_PHONE_NUMBER
    TO_NUMBER = SCHOOL_PHONE_NUMBER

    @classmethod
    def validate(cls) -> list[str]:
        """Validate all required environment variables are present.

        Returns:
            list[str]: Names of missing required variables. Empty if all present.
        """
        required_vars = [
            "TWILIO_ACCOUNT_SID",
            "TWILIO_AUTH_TOKEN",
            "MY_PHONE_NUMBER",
            "TWILIO_PHONE_NUMBER",
            "DAD_PHONE_NUMBER",
            "SCHOOL_PHONE_NUMBER",
            "SKIP_CALENDAR_ID",
        ]
        missing = [var for var in required_vars if not getattr(cls, var)]
        return missing


# Validate on import
if missing := Config.validate():
    raise EnvironmentError(f"Missing required config: {', '.join(missing)}")
