from dotenv import load_dotenv
import os
import json
import requests
import re
url = 'https://api.kulturpool.at/search'


def find_number_of_results(name):
    """
    takes query and checks how many search results exist in Kulturpool
    :param name: str, query string
    :return: int, number of search results"""

    params = {
        'q': name,
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data["found"]


def get_data_of_page(name, page):
    """
    Gets results from page "page" of the Kulturpool
    :param name: str, query string
    :param page: int, page number
    :return: return json file as detailed in the documentation of the Kulturpool API.
    """
    params = {
        'q': name,
        'page': page
    }
    response = requests.get(url, params=params)
    return response.json()


def get_all_info(name, n=50):
    """
    Collects the n first results from Kulturpool.
    :param name: str, query string
    :param n: int, number of results wanted
    :return: two dictionnaries. text_dict has the form {'id': 'text'},
            info_dict the form {'id': ['title', 'previewImage', 'isShownAt']}
    """
    number_of_results = find_number_of_results(name)
    print(f'Number of results found: {number_of_results}')

    text_dict = dict()
    info_dict = dict()
    for i in range(1, min(number_of_results, n) // 20 + 2):
        data = get_data_of_page(name, i)
        for hit in data['hits']:
            doc = hit['document']
            if doc['description']:
                text_dict[doc['id']] = doc['title'][0] + ' ' + doc['description'][0]
            else:
                text_dict[doc['id'][0]] = doc['title'][0]
            if 'previewImage' in doc.keys():
                info_dict[doc['id']] = [doc['title'][0], doc['previewImage'], doc['isShownAt']]
            else:
                info_dict[doc['id']] = [doc['title'][0], '', doc['isShownAt']]
    return text_dict, info_dict


def get_prompt(input_text, data):
    """
    returns prompt for 'api_call'
    :param input_text: str, text for which similar matches should be found
    :param data: dictionary of the form {'id', 'text'}
    :return: str, prompt to be given to the API.
    """
    prompt = f"""
    **Instructions:**
    You are given an input text describing a certain entity (e.g. a person, an event, a place): {input_text}
    You are also given a dictionary of comparison media objects, where the keys are IDs and the values are descriptions of the media objects: {data}

    Your task is to identify the most relevant comparison media objects for the input entity.
    - First, prioritize direct depictions of the entity (e.g. portraits, photographs, images, or other visual representations).
    - Then, include additional objects that provide *different but still relevant* information (e.g. related events, associated locations, important documents, or contextual material).
    - Avoid returning only one type of object; aim for a well-rounded selection that covers multiple aspects of the entity.
    - Rank the selected objects from most to least relevant, with direct depictions first.
    - Return a list of the IDs of the most relevant comparison objects in order.
    - The JSON format must be valid.
    - DO NOT include any Markdown, code blocks, or extra text.

    {{
      "most_relevant": [],
      "explanations": {{}}
    }}
    """
    return prompt

def api_call(text, data):
    """
    performs API call.
    :param text: str, text for which similar matches should be found
    :param data: dictionary of the form {'id', 'text'}
    :return: list of "most relevant ids". list of str, each string is an id
    """
    load_dotenv()
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    print(f"API Key loaded: {OPENROUTER_API_KEY is not None}")
    prompt = get_prompt(text, data)

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
    result = response.json()['choices'][0]['message']['content']
    keys_list = re.findall(r'"([0-9a-f]{24})"', result)

    keys_list = list(set(keys_list))
    return_list = []
    for i in range(min(len(keys_list),9)):
        return_list.append(keys_list[i])
    return return_list

def get_relevant(name, description):
    """
    For a name 'name' get_relevant queries data from Kulturpool (combining title and description),
    then it builds a prompt, combining the description 'description' with the data from Kulturpool.
    Finally, it returns up to 9 "most relevant" samples from Kulturpool.
    :param name: str, query string
    :param description: str, description of the entity
    :return: list of dictionaries of the form:
            [{'id':value, 'title': value, 'previewImage': value, 'isShownAt': value}, {}, ...]
    """
    print("let's get the most relevant media objects!")
    data, info = get_all_info(name)
    relevant_examples = api_call(description, data)
    res_list = []
    for k in relevant_examples:
        if k in info.keys():
            d = {}
            d['id'] = k
            d['title'] = info[k][0]
            d['previewImage'] = info[k][1]
            d['isShownAt'] = info[k][2]
            res_list.append(d)
    return res_list
