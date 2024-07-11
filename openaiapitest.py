# file: openai_api_test.py
from dotenv import load_dotenv
import os
import openai
import httpx

# Load environment variables
load_dotenv()
API_KEY = os.environ.get('OPEN_API_KEY')

if not API_KEY:
    raise ValueError("API key not found in environment variables.")

# Create a custom HTTPX client with SSL verification disabled
httpx_client = httpx.Client(verify=False)

# Custom function to handle the request using the custom HTTPX client
def create_assistant():
    url = "https://api.openai.com/v1/assistants"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "OpenAI-Beta": "assistants=v2"
    }
    data = {
        "instructions": "You are a wine somlier. You should tell me about wine information and translate it in Korean.",
        "name": "WineCuration",
        "tools": [],
        "model": "gpt-4-turbo"
    }

    try:
        response = httpx_client.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()
    except httpx.HTTPStatusError as e:
        print(f"HTTP status error: {e.response.status_code} - {e.response.text}")
    except httpx.RequestError as e:
        print(f"Request error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def create_thread():
    url = "https://api.openai.com/v1/assistants"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "OpenAI-Beta": "assistants=v2"
    }
    data = {
        "instructions": "You are a wine somlier. You should tell me about wine information and translate it in Korean.",
        "name": "WineCuration",
        "tools": [],
        "model": "gpt-4-turbo"
    }

    try:
        response = httpx_client.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()
    except httpx.HTTPStatusError as e:
        print(f"HTTP status error: {e.response.status_code} - {e.response.text}")
    except httpx.RequestError as e:
        print(f"Request error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Create the assistant
my_assistant = create_assistant()
if my_assistant:
    print(my_assistant)
else:
    print("Failed to create the assistant.")


# assistant 'id': 'asst_hnFiTxrqdeWTB0nHRTDBee51'

# Create thread
client = openai.OpenAI()
empty_thread = client.beta.threads.create()
print(empty_thread)