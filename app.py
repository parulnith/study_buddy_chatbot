from __future__ import annotations
from typing import List, Tuple, Dict, Any
from collections import deque
import os
import time
import gradio as gr
from dotenv import load_dotenv
from google import genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch
import PIL.Image
from io import BytesIO

# Constants
SYSTEM_PROMPT = """
You are a friendly AI study buddy for kids under 12. You must:
- Only answer study-related questions.
- Avoid topics related to video games, violence, movies, or social media.
- Encourage learning in a fun and engaging way.
- Provide clear, simple explanations.
- Answer questions about images if uploaded.
- You can answer relevant current affairs questions.
"""

RESTRICTED_TOPICS = ["games", "violence", "movies", "social media", "video games"]
MAX_CHAT_HISTORY = 10

# Initialize Gemini client
def initialize_client() -> genai.Client:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("❌ Error: GEMINI_API_KEY not found in environment variables!")
    return genai.Client(api_key=api_key)

# Manage chat history
class ChatSessionManager:
    def __init__(self):
        self.sessions = deque(maxlen=MAX_CHAT_HISTORY)
        self.titles = deque(maxlen=MAX_CHAT_HISTORY)

    def add_session(self, history: List[Dict[str, str]], title: str) -> None:
        self.sessions.append(history.copy())
        self.titles.append(title)

    def get_session(self, index: int) -> List[Dict[str, str]]:
        if 0 <= index < len(self.sessions):
            return self.sessions[index]
        return [{"role": "assistant", "content": "👋 Hi there! What's your name? 😊"}]

    def get_titles(self) -> list:
        return list(self.titles)

# Process user messages
def process_message(
    message: str,
    image,
    chat_history: List[Dict[str, str]],
    grounding_enabled: bool,
    kid_name: str,
    client: genai.Client,
    session_manager: ChatSessionManager,
) -> Tuple[str, List[Dict[str, str]], str, list, Any]:
    if not message.strip() and image is None:
        return "", chat_history, kid_name, session_manager.get_titles(), image

    if not kid_name:
        kid_name = message.strip()
        chat_history.extend([
            {"role": "user", "content": message},
            {"role": "assistant", "content": f"Nice to meet you, {message}! 😊 What do you want to learn today?"},
        ])
        return "", chat_history, kid_name, session_manager.get_titles(), image

    user_message = f"{kid_name}: {message}"
    if image is not None:
        user_message += " [Image uploaded]"

    chat_history.append({"role": "user", "content": user_message})
    chat_history.append({"role": "assistant", "content": "Thinking... 🤖"})

    if any(topic in message.lower() for topic in RESTRICTED_TOPICS):
        chat_history[-1] = {
            "role": "assistant",
            "content": f"🙅‍♂️ Sorry {kid_name}, I can only help with studies! 📚 Let's focus on learning. 😊",
        }
        return "", chat_history, kid_name, session_manager.get_titles(), image

    try:
        tools = [Tool(google_search=GoogleSearch())] if grounding_enabled else []
        generation_config = GenerateContentConfig(
            tools=tools,
            response_modalities=["TEXT"],
            system_instruction=SYSTEM_PROMPT
        )
        if image is not None:
            img_byte_arr = BytesIO()
            image.save(img_byte_arr, format="PNG")
            img_bytes = img_byte_arr.getvalue()
            contents = [{"role": "user", "parts": [{"text": message}, {"inline_data": {"mime_type": "image/png", "data": img_bytes}}]}]
        else:
            contents = [{"role": "user", "parts": [{"text": message}]}]

        #model = client.models("gemini-2.0-flash")
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=contents,
            config=generation_config)
        

        reply = f"🤖 {kid_name}, " + response.candidates[0].content.parts[0].text
        chat_history[-1] = {"role": "assistant", "content": reply}

    except Exception as e:
        chat_history[-1] = {
            "role": "assistant",
            "content": f"🤖 Oops {kid_name}, something went wrong! Let's try again. 😊 Error: {str(e)}",
        }

    return "", chat_history, kid_name, session_manager.get_titles(), image

# Create Gradio UI
def create_interface(client: genai.Client, session_manager: ChatSessionManager) -> gr.Blocks:
    custom_css = """
    body {
        background-color: #FFE5B4;
    }
    .sample-questions-row {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-bottom: 5px;
    }
    button.sample-questions {
        flex: 1 !important;
        border-radius: 8px !important;
        border: none !important;
        color: black !important;
        padding: 6px 8px !important;
        font-size: 0.9rem !important;
        height: 50px !important;
        min-height: 34px !important;
        line-height: 3 !important;
        text-align: center !important;
    }
    button.sample-questions:hover {
        background-color: #FF6F61 !important;
    }
    #chatbot {
        min-height: 580px;
        max-height: 700px;
        overflow-y: auto;
        border-radius: 10px;
        background-color: #FFF3E0;
        padding: 10px;
    }
    #prev-chats-container {
        height: 500px;
        overflow-y: scroll;
        background: #FFF8E1;
        border-radius: 10px;
        padding: 5px;
    }
    #notes {
        background: #FFF8E1;
        border-radius: 10px;
    }
    #prev-chats-container .gradio-radio-option,
    #prev-chats-container label {
        display: block !important;
        width: 300px !important;
        margin-bottom: 10px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    #load-btn {
        
        font-size: 16px !important;
        height: 10px !important;
        
    }
    #large-image-box {
        width: 100% !important;
        min-height: 400px;
        object-fit: cover;
        border-radius: 8px;
    }
    """

    with gr.Blocks(fill_height=True, theme="soft", css=custom_css) as demo:
        with gr.Row(equal_height=True):
            with gr.Column(scale=2, min_width=350):
                gr.Markdown("")
                with gr.Column(elem_id="prev-chats-container"):
                    prev_chats = gr.Radio(choices=session_manager.get_titles(), label="💬 Previous Chats")
                load_btn = gr.Button("🔄 Load Chat", size="sm", elem_id="load-btn")
                todo_list = gr.Textbox(placeholder="Write your Notes here...", lines=15, label="📋 My Notes", show_copy_button=True, elem_id="notes")
            with gr.Column(scale=10):
                gr.Markdown("<h1 style='text-align: center;'> 📚 Study Buddy - AI Learning Friend! 🤖</h1>")
                chatbot = gr.Chatbot(value=[{"role": "assistant", "content": "👋 Hi there! What's your name? 😊"}], type="messages", elem_id="chatbot", scale=5)
                msg = gr.Textbox(placeholder="Type here...", label="Your Message", lines=1, scale=4)

                with gr.Row():
                    # Left Column: Sample Questions + Clear Chat
                    with gr.Column(scale=3):
                        with gr.Row(elem_id="sample-questions", elem_classes=["sample-questions-row"]):
                            q1 = gr.Button("Create a spelling challenge for me.", elem_classes=["sample-questions"])
                            q2 = gr.Button("Test my knowledge of world geography.", elem_classes=["sample-questions"])
                            q3 = gr.Button("How can I improve my vocabulary", elem_classes=["sample-questions"])
                        with gr.Row(elem_id="sample-questions", elem_classes=["sample-questions-row"]):
                            q4 = gr.Button("Generate a quiz on", elem_classes=["sample-questions"])
                            q5 = gr.Button("Suggest a daily study routine", elem_classes=["sample-questions"])
                            q6 = gr.Button("Explain the Concept of", elem_classes=["sample-questions"])
                        with gr.Row(elem_id="sample-questions", elem_classes=["sample-questions-row"]):
                            q7 = gr.Button("Tips to stay focused while studying", elem_classes=["sample-questions"])
                            q8 = gr.Button("Plan my homework & study time", elem_classes=["sample-questions"])
                            q9 = gr.Button("Generate a lesson plan.", elem_classes=["sample-questions"])
                   

                    with gr.Column(scale=4):
                        image_input = gr.Image(
                            label="Upload a picture to ask about",
                            type="pil",
                            sources=["upload"],
                            elem_id="large-image-box",
                            width=800,
                            height=300
                        )


                
                with gr.Row():
                    clear_btn = gr.Button("🗑️ Clear Chat")
                    ground_btn = gr.Button("🔍 Enable Grounding")

                kid_name = gr.State("")
                grounding_state = gr.State(False)

                def toggle_grounding(state):
                    new_state = not state
                    new_label = "🔍 Disable Grounding" if new_state else "🔍 Enable Grounding"
                    return new_state, new_label

                ground_btn.click(toggle_grounding, inputs=[grounding_state], outputs=[grounding_state, ground_btn])

                def clear_chat(chat_history, kid):
                    return ([{"role": "assistant", "content": "👋 Hi there! What's your name? 😊"}], "", gr.update(choices=session_manager.get_titles()), None, "")

                clear_btn.click(clear_chat, inputs=[chatbot, kid_name], outputs=[chatbot, msg, prev_chats, image_input, kid_name])

                msg.submit(
                    lambda message, image, chat_history, kid, grounding_on: process_message(message, image, chat_history, grounding_on, kid, client, session_manager),
                    inputs=[msg, image_input, chatbot, kid_name, grounding_state],
                    outputs=[msg, chatbot, kid_name, prev_chats, image_input]
                )

                load_btn.click(lambda selected: session_manager.get_session(session_manager.titles.index(selected)) if selected else [{"role": "assistant", "content": "👋 Hi there! What's your name? 😊"}], prev_chats, chatbot)

                q1.click(lambda: "Create a spelling challenge for me.", None, msg)
                q2.click(lambda: "Test my knowledge of world geography.", None, msg)
                q3.click(lambda: "How can I improve my vocabulary?", None, msg)
                q4.click(lambda: "Generate a quiz for me on", None, msg)
                q5.click(lambda: "Suggest a daily study routine for me.", None, msg)
                q6.click(lambda: "Explain the Concept of", None, msg)
                q7.click(lambda: "Tips to stay focused while studying", None, msg)
                q8.click(lambda: "Plan my homework and study time", None, msg)
                q9.click(lambda: "Generate a lesson plan for me", None, msg)

        return demo

# --- main function ---
def main():
    client = initialize_client()
    session_manager = ChatSessionManager()
    demo = create_interface(client, session_manager)
    demo.launch()

if __name__ == "__main__":
    main()
