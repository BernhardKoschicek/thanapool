import ast
from dotenv import load_dotenv
import os
import requests
import json

def get_prompt(text):
    prompt = f"""
    **Instructions:**
    Analyze the text {text}.
    Extract keywords in the categories given. Return ONLY a Python dictionary in this exact format 
    (without any extra text, quotes around keys are optional):

    "person_names": ["Name1", "Name2"],
    "place_names": ["Place1", "Place2"],
    "dates": ["Date1", "Date2"]

    Return ONLY a valid Python dictionary in exactly the following format 
    (no spaces or newlines!). <value> must always be a list of strings.
    {{'person_names': <value>, 'place_names': <value>, 'dates': <value>}}
    """
    return prompt

def check_if_dict(output):
    valid = False
    limit = 5
    counter = 0
    while not valid and counter != limit:
        print(counter)
        counter += 1
        try:
            data = ast.literal_eval(output)
            if isinstance(data, dict):
                print("Success: valid dictionary")
                print(output)
                result = data
                valid = True
            else:
                print("Parsed object is not a dictionary")
                print(output)
                result = None
        except Exception as e:
            print("Failed to parse:", e)
            print(output)
            result = None
    return result

def openrouter_call(text):
    load_dotenv()
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    print(f"API Key loaded: {OPENROUTER_API_KEY is not None}")
    prompt = get_prompt(text)

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
                    "content": prompt
                }
            ]
        })
    )
    output = response.json()['choices'][0]['message']['content']
    return check_if_dict(output)
    #return output
