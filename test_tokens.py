#!/usr/bin/env python3

import openai
import base64
import re

def encode_image_to_base64(image_path):
    """Encodes an image file to a Base64 data URI."""
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return f"data:image/jpeg;base64,{encoded_string}"

def get_exact_image_tokens(image_path, text_prompt):
    """Get exact image token count using vLLM's tokenizer"""
    try:
        # Create a minimal request to get token count
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": text_prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": encode_image_to_base64(image_path)
                        }
                    }
                ]
            }
        ]
        
        # Try to make a request with max_tokens=1 to get token count info
        try:
            response = client.chat.completions.create(
                model="Qwen/Qwen2.5-VL-3B-Instruct",
                messages=messages,
                max_tokens=1
            )
            print("✅ Request succeeded - input fits in context")
            return None  # We can't get exact count this way
        except Exception as e:
            error_msg = str(e)
            print(f"Error message: {error_msg}")
            
            # Parse error message for token count
            if "length" in error_msg and "tokens" in error_msg:
                # Extract token count from error message
                match = re.search(r'length (\d+)', error_msg)
                if match:
                    total_tokens = int(match.group(1))
                    print(f"📊 Total input tokens (from error): {total_tokens}")
                    return total_tokens
            
            return None
            
    except Exception as e:
        print(f"Error getting exact token count: {e}")
        return None

# Setup client
client = openai.OpenAI(
    base_url="http://localhost:8801/v1",
    api_key="not-needed"
)

# Test with your image
image_path = "/mnt/storage1/shourovj/vllm_inference/pres_images/image (3).webp"
text_prompt = "Extract all the medcine informations in a structured json format"

print("🔍 Getting exact token count from vLLM server...")
exact_tokens = get_exact_image_tokens(image_path, text_prompt)

if exact_tokens:
    print(f"\n📊 Exact total input tokens: {exact_tokens}")
    
    # Count text tokens separately
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-VL-3B-Instruct")
    text_tokens = len(tokenizer.encode(text_prompt))
    image_tokens = exact_tokens - text_tokens
    
    print(f"📝 Text tokens: {text_tokens}")
    print(f"🖼️  Image tokens: {image_tokens}")
    
    # Check against model limit
    max_model_len = 1024
    available_for_output = max_model_len - exact_tokens
    
    print(f"\n📏 Model context limit: {max_model_len} tokens")
    print(f"📊 Available for output: {available_for_output} tokens")
    
    if exact_tokens > max_model_len:
        print(f"❌ Input too large! Need {exact_tokens} tokens but model only supports {max_model_len}")
        print("💡 Solution: Increase --max-model-len when starting vLLM server")
    else:
        print(f"✅ Input fits! Can generate up to {available_for_output} tokens")
else:
    print("❌ Could not get exact token count")
