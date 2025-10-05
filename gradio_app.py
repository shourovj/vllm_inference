import gradio as gr
import openai
import base64
import time
import os
from typing import List, Tuple

# --- Image Encoding Function ---
def encode_image_to_base64(image_path):
    """Encodes an image file to a Base64 data URI."""
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return f"data:image/jpeg;base64,{encoded_string}"

# --- vLLM Client Setup ---
# Use environment variable for backend URL, fallback to localhost
import os
backend_url = os.getenv("BACKEND_URL", "http://localhost:8801")

client = openai.OpenAI(
    base_url=f"{backend_url}/v1",
    api_key="not-needed"
)

# --- Chat History Storage ---
chat_history = []

def process_image_with_text(image, text_prompt: str, history: List) -> Tuple[str, List]:
    """Process image with text prompt and return response with updated history"""
    if image is None:
        return "Please upload an image first.", history
    
    if not text_prompt.strip():
        return "Please enter a text prompt.", history
    
    try:
        # Encode image to base64
        base64_image_uri = encode_image_to_base64(image)
        
        # Create the API request
        start_time = time.time()
        completion = client.chat.completions.create(
            model="Qwen/Qwen2.5-VL-3B-Instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": text_prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": base64_image_uri
                            }
                        }
                    ]
                }
            ],
            max_tokens=400
        )
        
        response = completion.choices[0].message.content
        end_time = time.time()
        
        # Add to chat history in the correct format for messages type
        history.append({"role": "user", "content": text_prompt})
        history.append({"role": "assistant", "content": response})
        
        # Add processing time info
        processing_time = f"\n\n⏱️ Processing time: {end_time - start_time:.2f} seconds"
        
        return response + processing_time, history
        
    except Exception as e:
        error_msg = f"Error processing request: {str(e)}"
        history.append({"role": "user", "content": text_prompt})
        history.append({"role": "assistant", "content": error_msg})
        return error_msg, history

def clear_chat_history():
    """Clear the chat history"""
    return [], []

def save_chat_history(history):
    """Save chat history to a file"""
    if not history:
        return "No chat history to save."
    
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"chat_history_.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("vLLM Inference Chat History\n")
        f.write("=" * 50 + "\n\n")
        
        conversation_count = 1
        for i in range(0, len(history), 2):
            if i + 1 < len(history):
                user_msg = history[i]
                assistant_msg = history[i + 1]
                f.write(f"Conversation {conversation_count}:\n")
                f.write(f"User: {user_msg['content']}\n")
                f.write(f"Assistant: {assistant_msg['content']}\n")
                f.write("-" * 30 + "\n\n")
                conversation_count += 1
    
    return f"Chat history saved to {filename}"



# --- Gradio Interface ---
def create_gradio_interface():
    with gr.Blocks(title="vLLM Vision Inference", theme=gr.themes.Soft()) as interface:
        gr.Markdown(
            """
            # 🖼️ vLLM Vision Inference Interface
            
            Upload an image and ask questions about it using the Qwen2.5-VL-3B-Instruct model.
            """
        )
        
        with gr.Row():
            with gr.Column(scale=1):
                # Image upload
                image_input = gr.Image(
                    label="Upload Image",
                    type="filepath",
                    height=400
                )
                
                # Text input
                text_input = gr.Textbox(
                    label="Text Prompt",
                    placeholder="Enter your question about the image...",
                    lines=3,
                    value="Extract all the medicine informations in a structured json format"
                )
                
                # Buttons
                with gr.Row():
                    submit_btn = gr.Button("🚀 Process Image", variant="primary")
                    clear_btn = gr.Button("🗑️ Clear Chat", variant="secondary")
                    save_btn = gr.Button("💾 Save History", variant="secondary")
                
                # Status
                status_output = gr.Textbox(
                    label="Status",
                    interactive=False,
                    lines=2
                )
            
            with gr.Column(scale=2):
                # Chat history
                chat_output = gr.Chatbot(
                    label="Chat History",
                    height=500,
                    show_label=True,
                    container=True,
                    bubble_full_width=False,
                    type="messages"
                )
        
        # Event handlers
        submit_btn.click(
            fn=process_image_with_text,
            inputs=[image_input, text_input, chat_output],
            outputs=[status_output, chat_output],
            show_progress=True
        )
        
        clear_btn.click(
            fn=clear_chat_history,
            outputs=[chat_output, status_output]
        )
        
        save_btn.click(
            fn=save_chat_history,
            inputs=[chat_output],
            outputs=[status_output]
        )
        
        # Example prompts
        gr.Markdown(
            """
            ## 💡 Example Prompts:
            - "Extract all the medicine informations in a structured json format"
            - "Describe what you see in this image"
            - "What are the main objects in this image?"
            - "Analyze the text in this image"
            - "What is the purpose of this document?"
            """
        )
    
    return interface

# --- Main Function ---
if __name__ == "__main__":
    # Create and launch the interface
    interface = create_gradio_interface()
    interface.launch(
        server_name="0.0.0.0",  # Allow external access
        server_port=7860,      # Default Gradio port
        share=False,           # Set to True if you want a public link
        debug=True
    )
