# Skipper

**An intelligent pipeline that uses AI and voice cloning to automate professional absence notifications.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-In%20Development-orange.svg)](https://github.com/your-username)

---

### 🎯 Overview

Skipper is a robust Python application that automates the entire process of notifying the office about planned absences. By integrating Google Calendar data with advanced AI and voice cloning technology, Skipper transforms tedious manual administration into a single, automated workflow. It is designed to deliver professional and context-aware notifications efficiently.

---

### ✨ Key Features

Skipper is built on a pipeline that delivers precision and realism:

- **Intelligent Scheduling:** Scrapes Google Calendar data to accurately identify planned absences for the upcoming work week.
- **AI-Powered Scripting:** Utilizes a Large Language Model (LLM) to dynamically generate context-aware calling scripts, ensuring the tone is professional and appropriate.
- **High-Fidelity Voice Cloning:** Employs MLX Audio and TTS to clone a reference voice, creating realistic and personalized audio notifications.
- **Automated Communication:** Integrates with the Twilio API to manage the entire outbound calling process.
- **Precise Scheduling Logic:** Implements advanced time logic to schedule notifications precisely for optimal timing (e.g., Monday mornings or preceding Friday).
- **Secure & Local Workflow:** Manages all sensitive data and processing locally, prioritizing data privacy and security.

---

### 🛠️ Getting Started: Deployment Guide

Follow these steps to set up and run Skipper on your local environment.

#### Prerequisites (Required Tools)

Ensure you have the following tools and accounts ready:

- **Python 3.x:** The core execution environment.
- **Ollama:** Required to run the local LLM engine (e.g., Qwen).
- **Twilio Account:** Needed for executing external outbound calls.
- **Google Calendar Access:** Credentials must grant read access to your schedule.
- **MLX Audio Environment:** Essential for the voice cloning component.

#### Installation Steps

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/your-username/skipper.git
    cd skipper
    ```

2.  **Install Dependencies:**
    Install all required Python libraries:

    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment Variables (Secrets Management):**
    Create a file named `.env` in the root directory to securely store all sensitive credentials. **Never commit this file.**

    **`.env` Example:**

    ```env
    # Twilio Credentials
    TWILIO_ACCOUNT_SID="ACxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    TWILIO_AUTH_TOKEN="your_auth_token_here"
    MY_PHONE_NUMBER="+1234567890"
    SCHOOL_PHONE_NUMBER="+19876543210"
    DAD_PHONE_NUMBER="+1122334455"

    # Application Configuration
    NGROK_URL="https://incubous-caitlyn-herby.ngrok-free.dev"
    OUTPUT_FILE_DIRECTORY="./output_audios"
    ```

4.  **Execute the System:**
    Run the main script to initiate the full automated workflow:
    ```bash
    python main.py
    ```

---

### 🧠 Architecture: The System Blueprint

Skipper is built as a modular pipeline, ensuring every step is handled efficiently and securely:

1.  **Data Ingestion (`calendar_scraper.py`):** Interfaces with the Google Calendar API to reliably extract absence data for the target work week.
2.  **Contextual Generation (`generate_phrase.py`):** The schedule data is fed to the LLM (Ollama) to generate a context-aware, natural calling script, adhering to predefined rules.
3.  **Voice Synthesis (`generate_audio.py`):** Uses MLX Audio and the Qwen TTS model to clone a reference voice, creating high-fidelity, realistic audio files.
4.  **Web Service (`app.py`):** Functions as the secure backend Flask server, providing a dedicated endpoint for Twilio to request the synthesized audio securely.
5.  **Orchestration (`main.py`):** The central controller that orchestrates the entire flow, connecting data retrieval, AI scripting, audio generation, and the final Twilio API call.

---

### 🗺️ Roadmap: Future Enhancements

We are focused on expanding Skipper's control and flexibility for future releases:

- **Precision Scheduling:** Implement precise time logic to schedule notifications for specific, optimal windows (e.g., Monday mornings or preceding Friday).
- **Voice Diversity Protocol:** Implement multi-voice cloning to allow for more flexible and personalized notification delivery.
- **Emergency Override:** Develop an on-demand function for emergency calls, allowing for manual intervention when needed.
- **Enhanced Verification:** Integrate real-time phone number verification with Twilio to enhance security and masking protocols.
- **Real-time Monitoring:** Implement improved logging to provide clear, real-time status updates for seamless debugging.

---

### 🤝 Contributing

We welcome contributions! If you have bug reports, feature ideas, or suggestions for improvement, please open an Issue or submit a Pull Request.

1.  Fork the repository.
2.  Create your feature branch.
3.  Commit your changes and open a Pull Request.

### 🔒 Security & Privacy: Data Integrity

Security is fundamental to Skipper's design. We prioritize data integrity above all else:

- **Credential Security:** All sensitive keys and phone numbers are stored exclusively in the **`.env`** file, ensuring they are not exposed in the code.
- **Local Processing:** All heavy AI and voice processing is executed locally on your machine, ensuring complete control and data privacy.
- **Security Posture:** We adhere to the principle of least privilege, ensuring the system operates with the minimum access necessary.
