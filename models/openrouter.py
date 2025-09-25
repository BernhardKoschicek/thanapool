from dotenv import load_dotenv
import os
import requests
import json


def openrouter_call():
    load_dotenv()
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    print(f"API Key loaded: {OPENROUTER_API_KEY is not None}")

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}"
        },
        data=json.dumps({
            "model": "openai/gpt-4o",
            "messages": [
                {
                    "role": "user",
                    "content": "What is the meaning of life?"
                }
            ]
        })
    )
    return response.json()['choices'][0]['message']['content']
