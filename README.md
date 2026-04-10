<!-- # Skipper
Automate the calling to the office to notify of absences, by reading my calendar for my schedule of absences.

How it works?
Connects to your Google Calendar via the calendar API, and scrapes the upcoming planned skips (absences) you have for the current week (or the following week if the current date is the weekend) from your SKIP calendar. Then it uses the relevant skip dates to dynamically generate a phrase, based off a set of safe constraints, using local AI enabled through AI. This script is then transcribed into your parent's voice through Blaizzy's MLX-Audio, specifically using Qwen's 1.7B TTS engine. Lastly, this file is saved to your computer, and then accessed by Twilio to play the audio, after a couple of delays and dials to your school's attendance system. Note: this project is currently designed to work by serving up a server for Twilio to access using Flask and ngrok. -->

# Skipper 🚪🏃🏽
**for when you finally realize school teaches jack******

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-In%20Development-orange.svg)](https://github.com/your-username)

---

### 🛑 The Mission (What Skipper Does)

Tired of boring, manual admin? Skipper is the ultimate system hack for life. It connects your calendar, uses cutting-edge AI voice cloning to call as your parents, automatically handling all the tedious calls about absences.

**The system's flawed, why not exploit it?**

---

### 🔥 Features: Your Toolkit for Control

We’ve built a system that doesn't just work—it dominates the process.

*   **Calendar Integration:** Reads your Google Calendar to locate all planned skips for the upcoming school week.
*   **AI Script Hacking:** Leverages a powerful LLM (Qwen) to generate natural, context-aware calling scripts, ensuring the tone is perfect for the task.
*   **Voice Clone Warfare (TTS):** Uses MLX Audio to clone a reference voice, allowing the system to deliver calls in a voice that sounds eerily real.
*   **Twilio Takeover:** Seamlessly integrates with the Twilio API to execute professional, automated outbound calls directly from your system.
*   **Smart Scheduling:** Implements complex time logic to schedule notifications perfectly for Monday mornings or the preceding Friday (6:00 AM - 7:00 AM).
*   **Stealth & Security:** Everything runs locally, ensuring your data is handled with maximum privacy and security.

### 🛠️ Getting Started: Deploying the Hack

Time to set up your command center. Follow these steps to activate Skipper.

#### Prerequisites (Your Gear)

You need the right tools to run this operation:

*   **Python 3.x:** The engine of the operation.
*   **Ollama:** Running your local, powerful LLM engine (like Qwen).
*   **Twilio Account:** Your portal to make calls to the real world.
*   **Google Calendar Access:** Credentials to view your schedule.
*   **MLX Audio Environment:** Necessary for the voice cloning magic.

#### Installation (The Setup)

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/your-username/skipper.git
    cd skipper
    ```

2.  **Install Dependencies:**
    Install the necessary libraries to bring the system to life:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Secrets (The `.env` File):**
    Create a file named `.env` in the root directory. **This is where you hide the sensitive keys.**

    **`.env` Example:**
    ```env
    # Twilio Credentials (Your Access Keys)
    TWILIO_ACCOUNT_SID="ACxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    TWILIO_AUTH_TOKEN="your_auth_token_here"
    MY_PHONE_NUMBER="+1234567890"
    SCHOOL_PHONE_NUMBER="+19876543210"
    DAD_PHONE_NUMBER="+1122334455"

    # System Configuration
    NGROK_URL="https://incubous-caitlyn-herby.ngrok-free.dev" # Keep your tunnel active!
    OUTPUT_FILE_DIRECTORY="./output_audios"
    ```

4.  **Run the Command:**
    Activate the system and launch the automation sequence:
    ```bash
    python main.py
    ```

### 🧱 Architecture: The Secret Blueprint

A pipeline designed for maximum efficiency and stealth.

1.  **Calendar Scraping (`calendar_scraper.py`):** We use the Google Calendar API to pull the target absence data for the most relevant school week.
2.  **AI Script Hacking (`generate_phrase.py`):** The absence data is fed to the LLM to generate a perfectly crafted, human-sounding script, obeying strict, rules defined in the System Prompt.
3.  **Voice Cloning Warfare (`generate_audio.py`):** The generated text is fed into the Qwen TTS model, cloning a reference voice (most likely your parent's) to create the final, believable audio file.
4.  **Web Portal (`app.py`):** This is the Flask server running behind ngrok, acting as the secure bridge that Twilio uses to request the synthesized audio.
5.  **Orchestration (`main.py`):** The master controller. It ties all the steps together, managing the flow from calendar scrape to voice delivery, and executes the final Twilio call.

### 🗺️ Roadmap: Leveling Up the Rebellion

The system is modular, and we are constantly working on features that give you ultimate control over this automation:

*   **Precision Scheduling:** Implement the hard-coded schedule: calls will automatically target Monday mornings or the preceding Friday (6 AM - 7 AM) for maximum impact.
*   **Voice Diversity Protocol:** Unlock the ability to clone multiple voices (Dad's and Mom's) to create perfectly masked, non-repetitive calls.
*   **Emergency Override Protocol:** Implement a dedicated, instant command to force an emergency call, bypassing the schedule for true last-minute control.
*   **Deep Masking:** Integrate phone number verification (via Twilio) to verify caller identities before dialing, making the automation practically invisible to oversight.
*   **Real-Time Debugging:** Enhance logging so you always know exactly what the system is doing, no guessing required.

### 🤝 Contributing

If you have a new exploit, a better idea, or want to help us level up the system, jump in!

1.  Fork the repository.
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`).
3.  Make your changes and commit them (`git commit -m 'Added some control'`).
4.  Push and open a Pull Request!

### 🔒 Security & Privacy: Keep the Secrets Hidden

Because this system handles real communication and personal data, security is non-negotiable.

*   **Secrets are King:** All sensitive tokens and phone numbers are stored exclusively in the **`.env`** file and are **never** committed to the repository.
*   **Local Processing:** All heavy AI and voice cloning operations happen locally, ensuring your data stays private and off the public internet.
*   **Rule Breaker:** **Never** hardcode API keys. Always use environment variables to keep your operational secrets safe.
