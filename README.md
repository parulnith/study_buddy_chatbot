# 📚 Study Buddy Chatbot

[![Python Version](https://img.shields.io/badge/Python-3.13%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) <!-- Assuming MIT License, replace if different -->

An interactive, kid-friendly study assistant chatbot built with Gradio and powered by Google's Gemini 2.0 Flash model. Designed to help children under 12 with their studies, especially during exam season.

Inspired by the need for a focused learning tool during India's exam season (typically March), this application provides an engaging way for kids to ask study-related questions, get explanations, and stay organized.

📢 **Check out the demo**: [Twitter Post](https://x.com/i/status/1894396963141087289)

## ✨ Key Features

*   **Interactive Chat Interface:** Built with Gradio for a user-friendly chat experience without complex UI code.
*   **AI-Powered Study Help:** Utilizes Google Gemini 2.0 Flash to answer study-related questions in a simple, engaging manner.
*   **Kid-Safe Content Filtering:** Designed to strictly answer study questions and avoid topics like gaming, violence, movies, or social media (enforced by system prompt and keyword filtering).
*   **Image Understanding:** Allows users to upload images (diagrams, charts, pictures in questions) for the AI to analyze and answer questions about.
*   **Multilingual Support:** Can handle queries in different languages, including Hindi (leveraging Gemini's capabilities).
*   **Real-time Information:** Optional grounding via Google Search allows the chatbot to fetch current affairs and fact-check information instantly.
*   **Chat History:** Remembers the conversation context within a session and allows loading previous chat sessions (up to a configurable limit).
*   **Integrated Notepad:** A simple text area for users to jot down quick study notes.
*   **Sample Prompts:** Quick-start buttons for common study-related queries.

## 🛠️ Tech Stack

*   **Python:** Core programming language.
*   **Gradio:** Framework for building the interactive web UI.
*   **Google Gemini API (generativeai):** Provides the AI model (Gemini 2.0 Flash) for chat responses and image understanding.
*   **python-dotenv:** For managing environment variables (like API keys).

## 📋 Requirements

*   **Python:** Version 3.13 or higher (as specified in `pyproject.toml` and `.python-version`).
*   **Google Gemini API Key:** You need an API key from Google AI Studio.
*   **Python Packages:** Listed in `pyproject.toml` and `uv.lock`. Key dependencies include:
    *   `google-genai>=1.2.0`
    *   `google-generativeai>=0.8.4`
    *   `gradio>=5.16.2`
    *   `python-dotenv>=1.0.1`
    *   `Pillow` (PIL fork, for image handling)

## 🚀 Installation

1.  **Clone the Repository:**
    ```bash
    git clone <https://github.com/parulnith/study_buddy_chatbot
    cd study-buddy-chatbot
    ```

2.  **Set up a Virtual Environment (Recommended):**
    ```bash
    # Using venv
    python -m venv venv
    source venv/bin/activate  # On Windows use `.venv\Scripts\activate`

    # Or using conda
    # conda create -n studybuddy python=3.13
    # conda activate studybuddy
    ```

3. **Install Dependencies:**
    Make sure your virtual environment is activated. Choose one of the following methods:

    *   **Using `pip` (installs required packages):**
        ```bash
        pip install google-genai gradio python-dotenv Pillow
        ```
        *(Note: This installs the dependencies listed in `pyproject.toml`)*

    *   **Using `uv` (for exact versions from `uv.lock`):**
        ```bash
        # Install uv if you haven't already: pip install uv
        uv pip sync
        ```

## ⚙️ Configuration

1.  **Obtain a Gemini API Key:** Visit [Google AI Studio](https://aistudio.google.com/app/apikey) to get your free API key.

2.  **Create a `.env` file:** In the root directory of the project, create a file named `.env`.

3.  **Add your API Key:** Add the following line to the `.env` file, replacing `<YOUR_API_KEY>` with the key you obtained:
    ```dotenv
    GEMINI_API_KEY=<YOUR_API_KEY>
    ```
   
## ▶️ Usage

1.  **Run the Application:**
    Make sure your virtual environment is activated and you are in the project's root directory.
    ```bash
    python app.py
    ```
   

2.  **Access the Interface:** Open your web browser and navigate to the local URL provided by Gradio (usually `http://127.0.0.1:7860`).

3.  **Interact with the Chatbot:**
    *   The chatbot will first ask for the user's name.
    *   Type study-related questions in the message box.
    *   Use the "Upload a picture" area to ask questions about images.
    *   Use the "My Notes" section for note-taking.
    *   Toggle the "Enable/Disable Grounding" button to control the use of Google Search for answers.
    *   Load previous conversations using the "Previous Chats" radio buttons and "Load Chat" button.
    *   Use the "Clear Chat" button to start a new conversation (the previous one will be saved if a name was entered).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue for bugs, feature requests, or improvements.


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. *(Create a LICENSE file if you intend to use MIT or another license)*

## 🙏 Acknowledgements

*   **Gradio Team:** For creating an easy-to-use framework for building ML web apps.
*   **Google:** For providing the powerful Gemini models.
