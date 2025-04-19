# 📚 Study Buddy Chatbot: A Friendly AI Learning Companion for kids, Powered by Google Gemini! 🤖

[![Python Version](https://img.shields.io/badge/Python-3.13%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Built with Gradio](https://img.shields.io/badge/Built%20with-Gradio-orange.svg)](https://www.gradio.app/)
[![Powered by Google Gemini](https://img.shields.io/badge/Powered%20by-Google%20Gemini-4285F4.svg)](https://ai.google.dev/)

**An interactive, safe, and engaging AI-powered chatbot designed as a study companion specifically for children under 12. Built using Python, Gradio, and leveraging the capabilities of Google's Gemini AI models.**

---

## 🌟 Introduction

Study Buddy is an AI chatbot that I created for my Kid to assist him during the exams. It leverages the power of **Google's Gemini models** to provide clear, simple explanations, while strict content filters and a carefully crafted persona ensure conversations remain appropriate and focused solely on learning. The intuitive interface, built with Gradio, allows kids to easily interact, ask questions about text or images, and even keep study notes, all within a single application.

📢 **See it in action!** [Check out the demo on Twitter](https://x.com/i/status/1894396963141087289)

<img width="1281" alt="Screenshot 2025-04-19 at 10 22 39 AM" src="https://github.com/user-attachments/assets/da371de4-7f35-4bed-959c-2fac56313059" />


## ✨ Key Features & Functionality

Study Buddy comes packed with features designed for an effective and enjoyable learning experience:

1.  **Interactive & Friendly Chat Interface:**
    * Built with **Gradio**, providing a clean, intuitive, and responsive web UI accessible from any browser
    * Features a familiar chat format that's easy for kids to use.
    * Starts by asking the child's name for a personalized touch (`kid_name` state).

2.  **AI-Powered Study Assistance (via Gemini):**
    * Utilizes **Google Gemini 2.0 Flash**, a powerful, efficient and low latency model from the Gemini family, to understand and respond to queries.
    * Answers a wide range of study-related questions (Math, Science, History, Geography, Language Arts, etc.).
    * Provides explanations in a simple, encouraging, and age-appropriate tone, as defined by the `SYSTEM_PROMPT`.

3.  **Kid-Safe Environment (Strict Content Filtering):**
    * **System Prompt Enforcement:** The Gemini model is explicitly instructed (`SYSTEM_PROMPT`) to *only* answer study-related questions and maintain a friendly, encouraging persona.
    * **Topic Restriction:** Explicitly blocks conversations related to sensitive or distracting topics like video games, violence, movies, or social media using a keyword filter (`RESTRICTED_TOPICS`).
    * **Polite Refusal:** If a restricted topic is detected, the chatbot gently redirects the user back to studying.

4.  **Multimodal Learning (Gemini Image Understanding):**
    * Leverages Gemini's native **multimodal capabilities**. Users can **upload images** (diagrams, textbook photos, math problems) via the `gr.Image` component.
    * The AI can analyze the uploaded image and answer questions related to its visual content.

5.  **Real-time Information & Fact-Checking (Gemini Grounding):**
    * Features an **"Enable/Disable Grounding"** toggle button (`ground_btn`).
    * When enabled, utilizes the **Grounding with Google Search** feature of the Gemini API to fetch up-to-date information and improve factual accuracy (see detailed section below).

6.  **Conversation Persistence & History:**
    * **Session Management:** Uses a `ChatSessionManager` to keep track of the current conversation history.
    * **Previous Chats:** Stores up to `MAX_CHAT_HISTORY` (currently 10) previous chat sessions.
    * **Load Chats:** Users can view titles of previous sessions and reload a past conversation.

7.  **Integrated Notepad:**
    * Includes a simple `gr.Textbox` labelled "My Notes" (`todo_list`) for quick note-taking during study sessions.

8.  **Sample Question Prompts:**
    * Provides several `gr.Button` examples (`q1` to `q9`) for common study requests to help users get started easily.

9.  **Clear Chat Functionality:**
    * A "Clear Chat" button (`clear_btn`) allows users to start a fresh conversation.

10. **Multilingual Capabilities:**
    * Inherits the strong multilingual capabilities of the Gemini model to potentially handle queries in various languages.

---

## ✨ Powered by Google Gemini  - Key Gemini Aspects Used:

* **Multimodality:** Study Buddy directly utilizes Gemini's ability to process both text prompts and **image inputs**. This allows students to upload pictures of diagrams, textbook pages, or visual problems and ask questions about them, creating a richer learning interaction than text-only chatbots.
* **Gemini 2.0 Flash Model:** We specifically use the `gemini-2.0-flash` model. This model is part of the latest Gemini generation and is optimized for **speed, efficiency, and cost-effectiveness**. It provides a great balance of performance and responsiveness, making it ideal for real-time conversational applications like this chatbot, while still supporting powerful features like long context and multimodality.
* **Core Intelligence:** Gemini serves as the "brain" of Study Buddy. It interprets user questions, retrieves relevant knowledge, follows the instructions set in the `SYSTEM_PROMPT` to maintain a kid-friendly persona, performs reasoning, generates helpful explanations, and powers the image analysis capabilities.


---

## 🌍 Real-time Information with Grounding

To ensure the information provided is accurate and up-to-date, Study Buddy incorporates the **Grounding with Google Search** feature available through the Gemini API.

**What is Grounding?**

Grounding connects the AI model's responses to external, verifiable sources of information – in this case, Google Search results. Instead of relying solely on the knowledge embedded during its training (which can become outdated), grounding allows the model to access and incorporate near real-time information from the web.

**How it Works Here:**

* **User Control:** The "Enable/Disable Grounding" button allows the user to toggle this feature.
* **Gemini API Tool:** When grounding is enabled, the application configures the Gemini API call to use the `GoogleSearch` tool (`Tool(Google Search=GoogleSearch())`).
* **API Process:** Before generating a response, the Gemini service uses Google Search to find information relevant to the user's query. This retrieved information is then used by the Gemini model to formulate a more accurate and current answer.

**Benefits for Study Buddy:**

* **Increased Accuracy:** Significantly reduces the chance of the model providing incorrect or "hallucinated" information, especially for factual queries.
* **Current Information:** Enables the chatbot to answer questions about recent events, discoveries, or topics that emerged after the model's last training update.
* **Enhanced Trustworthiness:** By basing answers on searchable web data, the responses become more reliable and trustworthy for educational purposes. (Note: While the API can return source links, this specific UI doesn't display them, but the underlying mechanism improves response quality).

This optional grounding feature makes Study Buddy a more robust and reliable learning tool, capable of accessing the breadth and freshness of Google Search when needed.

---

## 🛠️ Technology Stack

* **Core Language:** Python (3.13+)
* **Web UI Framework:** Gradio (`gradio`)
* **AI Model:** Google Gemini 2.0 Flash via the Google AI Python SDK (`google-genai`)
* **AI Features Used:** Text Generation, Multimodal Input (Image), Grounding (via Google Search Tool)
* **Environment Variables:** `python-dotenv`
* **Image Handling:** Pillow (`Pillow`)
* **Chat History Management:** Python `collections.deque`

---

## 📋 Prerequisites

* **Python:** Version 3.13 or higher.
* **Google Gemini API Key:** Essential for interacting with the Gemini model. Obtain one for free from [Google AI Studio](https://aistudio.google.com/app/apikey). Note the free tier limits and potential costs associated with features like grounding beyond the free quota.
* **Python Packages:** As listed below (can be installed via `pip` or `uv`).

---

## 🚀 Installation & Setup

1.  **Clone the Repository:**
    ```bash

    git clone https://github.com/parulnith/study_buddy_chatbot.git
    cd study-buddy-chatbot
    ```

2.  **Set up a Virtual Environment (Highly Recommended):**
    * *Using venv:*
        ```bash
        python -m venv venv
        source venv/bin/activate  # Linux/macOS
        # .\venv\Scripts\activate  # Windows
        ```
    * *Using conda:*
        ```bash
        conda create -n studybuddy python=3.13
        conda activate studybuddy
        ```

3.  **Install Dependencies:**
    Ensure your virtual environment is activated. Choose one method:
    * *Using pip (recommended for standard install):*
        ```bash
        pip install google-genai gradio python-dotenv Pillow
        ```
        *(Optionally, create a `requirements.txt` file: `pip freeze > requirements.txt` and then use `pip install -r requirements.txt`)*
    * *Using uv (if you have `uv.lock` for exact versions):*
        ```bash
        # Install uv first if needed: pip install uv
        uv pip sync
        ```

4.  **Configure API Key:**
    * Create a file named `.env` in the root directory of the project.
    * Add your Google Gemini API key to this file:
        ```dotenv
        # .env
        GEMINI_API_KEY=YOUR_ACTUAL_API_KEY_HERE
        ```
        Replace `YOUR_ACTUAL_API_KEY_HERE` with the key you obtained from Google AI Studio.

---

## ▶️ How to Run & Use

1.  **Start the Application:**
    * Make sure your virtual environment is activated.
    * Navigate to the project's root directory in your terminal.
    * Run the main script:
        ```bash
        python app.py
        ```

2.  **Access the Interface:**
    * Gradio will typically launch the app on a local URL like `http://127.0.0.1:7860`. Open this URL in your web browser.

3.  **Interact with Study Buddy:**
    * **Enter Name:** The chatbot will first ask for the user's name. Type the name and press Enter.
    * **Ask Questions:** Type any study-related question into the "Your Message" box and press Enter.
    * **Upload Images:** Click the "Upload a picture" area to select an image file from your device. Then, type your question related to the image in the message box and press Enter.
    * **Use Sample Prompts:** Click any of the buttons (e.g., "Explain the Concept of") to pre-fill the message box with that prompt.
    * **Use Notepad:** Type notes directly into the "My Notes" area. Use the copy button if needed.
    * **Toggle Grounding:** Click the "Enable/Disable Grounding" button to control whether the AI uses Google Search for answers. The button label indicates the current state. Be mindful of potential usage costs if exceeding free tiers.
    * **Manage Chats:** Use the "Previous Chats" list and "Load Chat" button to revisit past conversations. Use "Clear Chat" to start over.

---


## 🤝 Contributing

Contributions, feedback, and suggestions are welcome! Please open an Issue or submit a Pull Request.

---

## 📄 License

This project is licensed under the MIT License. 
