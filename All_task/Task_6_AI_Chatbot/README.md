# Task 6: AI Chatbot Application (GUI)

An intelligent, multi-mode Chatbot Application built using Python's standard `tkinter` library. It features a stunning bubble-chat interface modeled after Telegram and ChatGPT, complete with typing animations, timestamp metadata, asynchronous background processing, and optional Gemini LLM integration.

## Key Features

- **Modern Bubble Chat UI**:
  - **User Messages**: Aligned to the right inside a soft blue bubble (`#2b5278`) with white text and timestamps.
  - **Bot Messages**: Aligned to the left inside a dark slate bubble (`#182533`) with white text and timestamps.
  - **System Notifications**: Centered in italics for status updates.
- **Asynchronous Threading & Typing Animations**:
  - Network requests are processed in separate background threads, keeping the desktop window responsive.
  - While fetching the response, an animating typing bubble (`Typing ...`) appears on the left, making it feel like a real conversational chatbot.
- **Dual-Mode Operation**:
  - **Offline Helper Mode**: When no API key is supplied, the chatbot acts as a local assistant using keyword parsing and fuzzy matching algorithms (via Python's built-in `difflib`). It can guide users on internship details, recommend other tasks (like Tasks 2, 4, and 5), discuss PEP 8 rules, and tell programming jokes.
  - **Live AI Mode**: If a Google Gemini API Key is configured, the bot connects directly to Gemini 1.5 Flash models over secure HTTP REST requests, allowing open-ended discussions about programming concepts, debugging code, and general knowledge.
- **API Key Configuration Widget**: Allows users to save and configure their Gemini API Key inside a local config file directly in the app.

## Files

- `chatbot_app.py`: The Python application source code.
- `config.json`: Auto-generated configuration file storing the user's Gemini API key.

## How to Run

1. Open a terminal in the folder.
2. Run the application:
   ```bash
   python chatbot_app.py
   ```

## Dependencies
- Standard Python 3.x
- `requests` library (`pip install requests`)
