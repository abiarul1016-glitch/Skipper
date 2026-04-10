# 🚪🏃🏽 Skipper

**for when you finally realize school teaches jack\*\*\*\*.**

[![Prototype Demo](https://img.youtube.com/vi/Smu0lYzUtLI/maxresdefault.jpg)](https://www.youtube.com/watch?v=Smu0lYzUtLI)

---

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
[![Ollama](https://img.shields.io/badge/Ollama-fff?style=for-the-badge&logo=ollama&logoColor=000)](#)
[![Qwen](https://custom-icon-badges.demolab.com/badge/Qwen-605CEC?style=for-the-badge&logo=qwen&logoColor=fff)](#)
![Twilio](https://img.shields.io/badge/Twilio-API-blue?style=for-the-badge)
![Static Badge](https://img.shields.io/badge/twilio-red?style=for-the-badge&logo=https%3A%2F%2Fwww.svgrepo.com%2Fshow%2F354472%2Ftwilio-icon.svg&label=voice%20api)
![Static Badge](https://img.shields.io/badge/mlx_audio-orange?style=for-the-badge&label=voice%20cloning)
[![Flask](https://img.shields.io/badge/Flask-fff?style=for-the-badge&logo=flask)](#)

---

## What and why?

Skipping class too much, and constantly getting those calls home to your parents? Then having to manually call the school office—to confirm your absence? The endless loop of "Yes, my son was absent on Tuesday, and Wednesday, and Thursday..."? It's draining, repetitive, and utterly boring—school spoonfeeds, it's not our fault 🤷🏽‍♂️.

**Skipper** is the ultimate exploit, completely automating the process of notifying the school office of planned student absences by generating perfectly crafted, natural-sounding audio calls that sound exactly like your parent.

Instead of draining your (and your parents') time on a series of boring, scripted calls, you simply point it at your calendar, and **Skipper handles the communication, the scripting, and the voice delivery.**

Some people try to manage their time, others protect theirs—that's who Skipper is for.

---

## Features

- **Seamless Calendar Integration:** Automatically parses all planned absences from your Google Calendar, ensuring nothing falls through the cracks.
- **Context-Aware AI Scripting:** Uses local LLMs (Qwen via Ollama) to generate sophisticated, non-robotic scripts. The AI ensures the tone is perfect for the required administrative context.
- **Professional Voice Cloning (TTS):** Implements advanced voice cloning using MLX-Audio, delivering the message in a voice that is unnervingly believable.
- **Outbound Call Orchestration:** Integrates with the Twilio API to execute professional, timed, and scheduled outbound calls to the main office.
- **Secure Local Processing:** Everything runs entirely on your machine, ensuring that sensitive schedules and AI logic never touch the public cloud.
- **Smart Scheduling:** Time logic intelligently determines the optimal school week to call about, allowing you to plan weeks or months in advance.

---

## How it works

Skipper operates as a robust, multi-stage pipeline, moving from data ingestion to physical voice delivery with zero human intervention.

1. **Data Acquisition (`calendar_scraper.py`):** The system first accesses your Google Calendar API credentials to pull all scheduled absences for the target week. This is the core input data.
2. **Intelligent Script Generation (`generate_phrase.py`):** The raw absence data is then fed into the local LLM (Qwen). The LLM uses a highly constrained system prompt to transform simple dates into a natural, conversational script, guaranteeing context and tone.
3. **Audio Synthesis (`generate_audio.py`):** The generated text is immediately passed to the MLX-Audio pipeline. This model takes a reference voice sample and generates a high-fidelity audio file of the parent reading the script.
4. **Web Bridge (`app.py`):** A minimal Flask server runs behind `ngrok`. This server acts as a secure, accessible endpoint that Twilio can call, requesting the synthesized audio file based on a unique session ID.
5. **Orchestration & Delivery (`main.py`):** The main script coordinates the final action: triggering the Twilio API to make the outbound call, which connects to the Flask server to retrieve and play the pre-generated audio file. Both tracks of the call can be recorded to ensure the system works properly as well.

This multi-step process ensures that the call sounds authentic, the message is precise, and the technical workflow is robust.

---

## Tech stack

Skipper is a distributed, local-first system.

| Layer               | Technology      | Purpose                                                                               |
| :------------------ | :-------------- | :------------------------------------------------------------------------------------ |
| **Core Language**   | Python 3.x      | Orchestration, API scripting, and data handling.                                      |
| **Local AI/LLM**    | Ollama (Qwen)   | Runs the local Large Language Model for script generation.                            |
| **Voice Synthesis** | MLX-Audio       | Handles state-of-the-art, high-fidelity voice cloning (TTS).                          |
| **Communication**   | Twilio API      | The outbound call mechanism, connecting the system to the real world.                 |
| **Web Server**      | Flask / `ngrok` | Provides the necessary public-facing endpoint for Twilio to access the audio payload. |

---

## Running locally.

Before running, remember that this project requires several external services (Ollama, Twilio account, Google credentials) to be configured via the `.env` file.

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your-username/skipper.git
   cd skipper
   ```

2. **Install Dependencies:**
   This command installs all necessary Python libraries.

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables:**
   Create a file named `.env` and fill in all your credentials:

   ```env
   # Example .env structure
   TWILIO_ACCOUNT_SID="..."
   TWILIO_AUTH_TOKEN="..."
   # ... other keys
   ```

4. **Run the Automation:**
   Execute the main script to trigger the full cycle:
   ```bash
   python main.py
   ```
   _(Wait for the process to confirm the call was placed and the audio was delivered!)_

---

## What's next.

The system is inherently modular, and while it's functional now, the true potential is vast. Here's the roadmap to ultimate freedom:

- 📈 **Multi-Call Scheduling:** Implement advanced scheduling to call at random, non-robotic times to enhance realism.
- 🎙️ **Voice Profile Manager:** Allow switching between multiple parent voices with simple configuration changes.
- 🗓️ **Manual Override CLI:** Dedicated command-line tool to generate and play a single, emergency audio file without touching the calendar logic.
- ✉️ **Email Integration:** Expand functionality to handle notifications via automated email, reporting absences as well as calling.
- ⚙️ **Configurable Tone Profiles:** Allow defining different tones (e.g., "Very Concerned," "Mildly Casual," "Disappointed") for the AI script generator.

---

<div align="center">

the system's flawed. • why not exploit it? 🤷🏽‍♂️

</div>
