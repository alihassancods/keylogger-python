# Keylogger Python

A simple keylogger in Python that records keystrokes, saves them to a file, and sends the log as an email attachment using SendGrid.

## Features

- Captures all keystrokes (alphanumeric and special keys).
- Saves keystrokes to a timestamped file in a `files` directory.
- Sends the log file as an email attachment via SendGrid after execution.
- Uses environment variables for sensitive data (API keys and email addresses).

## Requirements

- Python 3.x
- The following Python packages:
  - `pynput`
  - `python-dotenv`
  - `sendgrid`
- A `.env` file with SendGrid API credentials and email addresses.

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/alihassancods/keylogger-python.git
   cd keylogger-python
   ```

2. **Install dependencies:**
   ```bash
   pip install pynput python-dotenv sendgrid
   ```

3. **Create a `.env` file** in the repository root with the following variables:
   ```
   SENDGRID_API_KEY=your_sendgrid_api_key
   FROM=your_sender_email@example.com
   RECIPIENT=your_recipient_email@example.com
   ```

4. **Create a `files` directory** to store log files:
   ```bash
   mkdir files
   ```

## Usage

Run the keylogger script:

```bash
python main.py
```

- The script will start listening for keystrokes.
- To stop logging, press the `Esc` key.
- After stopping, the script will email the keystroke log file as an attachment.

## How It Works

- The `Keylogger` class listens for keyboard events.
- Each keystroke is appended to a file named with the current date and time.
- When stopped, the script encodes the log file and sends it via SendGrid.
- Email addresses and API keys are securely loaded from the `.env` file.

## Disclaimer

This tool is intended for educational purposes only. Do **not** use it to log keystrokes without the user's explicit consent. Unauthorized use may violate local laws and ethical guidelines.
