import os
from dotenv import load_dotenv
from openai import OpenAI, AuthenticationError

# 1. Dynamically find the .env file
script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, '.env')

load_dotenv(dotenv_path=env_path)

def test_nvidia_nim_key():
    print("Testing NVIDIA NIM API Key...")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: NVIDIA_API_KEY is missing in the .env file.")
        return

    print("✅ Key found in .env file. Attempting to connect to NVIDIA NIM...")

    # 2. Initialize the OpenAI client but point it to NVIDIA's servers
    client = OpenAI(
        api_key=api_key,
        base_url="https://integrate.api.nvidia.com/v1"
    )

    try:
        # 3. Request a response from a fast NIM model
        response = client.chat.completions.create(
            model="meta/llama-3.1-8b-instruct",
            messages=[{"role": "user", "content": "Say 'Test successful' if you receive this."}],
            max_tokens=10
        )
        print("\n🎉 SUCCESS! Your NVIDIA API key is valid.")
        print(f"🤖 Agent Response: {response.choices[0].message.content}")
        
    except AuthenticationError as e:
        print("\n❌ AUTHENTICATION ERROR (401)")
        print("Your API key is invalid or typed incorrectly.")
        print(f"Details: {e}")
        
    except Exception as e:
        print("\n❌ UNEXPECTED ERROR")
        print(f"Details: {e}")

if __name__ == "__main__":
    test_nvidia_nim_key()