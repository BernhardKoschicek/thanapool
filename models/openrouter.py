import ast
from dotenv import load_dotenv
import os
import requests
import json

def get_prompt(text):
    prompt = f"""
    **Instructions:**
    Analyze the text: {text}
    Extract keywords in the following categories:
    
    - person_names
    - entity_names
    - place_names
    - dates
    - subject
    - material_information
    - actions
    
    Return ONLY a valid JSON object in the following format (keys must match exactly, values are lists of strings):
    - DO NOT wrap your output in markdown or code blocks.
    - DO NOT include extra text, explanations, or newlines.
    
    {{
      "person_names": [],
      "entity_names": [],
      "place_names": [],
      "dates": [],
      "taxonomic_subject": [],
      "typological_subject": [],
      "actions": []
    }}
    """

    return prompt

def check_if_dict(output, valid):
    try:
        data = ast.literal_eval(output)
        if isinstance(data, dict):
            result = data
            valid = True
        else:
            result = output
    except Exception as e:
        result = output
    return result, valid

def call_prompt(text):
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
    print(output)
    return output

def openrouter_call(text):
    output = call_prompt(text)
    valid = False

    limit = 5
    counter = 0
    while not valid and counter != limit:
        counter += 1
        result, valid = check_if_dict(output, valid)
        if not valid:
            output = call_prompt(text)

    if not valid:
        print('LLM was not able to generate the keyword-dictionary. See LLM-output below:')
        print(output)

    return result