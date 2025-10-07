import openai
import base64
import time

# --- Image Encoding Function ---
def encode_image_to_base64(image_path):
    """Encodes an image file to a Base64 data URI."""
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return f"data:image/jpeg;base64,{encoded_string}"



# --- Main Script ---
# 1. Point the client to your local server
client = openai.OpenAI(
    base_url="http://localhost:8801/v1",
    api_key="not-needed"
)


# 2. Define the path to your image and encode it
image_path = "/mnt/storage1/shourovj/vllm_inference/pres_images/image (3).webp"
base64_image_uri = encode_image_to_base64(image_path)


# 3. Create the API request with both text and image
start_time = time.time()
completion = client.chat.completions.create(
    model="Qwen/Qwen2.5-VL-3B-Instruct",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Extract all the medcine informations in a structured json format"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": base64_image_uri
                    }
                }
            ]
        }
    ],
    max_tokens=200
)

print(completion.choices[0].message.content)
end_time = time.time()
print(f"Time taken: {end_time - start_time} seconds")