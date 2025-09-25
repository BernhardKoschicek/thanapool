import requests
import re

# Base URL for Kulturpool API
BASE_URL = "https://api.kulturpool.at"

def kulturpool_search(item):
    response = requests.get(f"{BASE_URL}/search?q={item}")
    data = response.json()

    print(f"\nSuche nach: {item}")
    print("Gefunden:", data['found'])
    print("Seite:", data['page'])
    print("Suchzeit:", data['search_time_ms'], "ms")
    print("Anzahl Ergebnisse:", len(data['hits']))

    for i, hit in enumerate(data['hits']):
        obj = hit['document']
        print(f"{i + 1}. {obj.get('title', 'Kein Titel')}")
        if 'creator' in obj:
            print(f"   von {obj['creator']}")

def description_text(description):
    match = re.search(r"##de_##(.*?)##_de##", description, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None

def kulturpool_search_extended(openrouter_data):
    # loops
    for person in openrouter_data['person_names']:
        kulturpool_main(person)
    for place in openrouter_data['place_names']:
        kulturpool_main(place)
    for year in openrouter_data['dates']:
        kulturpool_main(year)

def extract_keywords(openrouter_data):
    keywords = []
    for values in openrouter_data.values():
        keywords.extend(values)
    keywords_all = " ".join(keywords)
    return keywords, keywords_all

def kulturpool_main(description, openrouter_data):
    # get description and try query with description
    descrip = description_text(description)
    result = kulturpool_search(descrip)
    if result:
        return result

    # get keywords and try with all keywords
    keywords, keywords_all = extract_keywords(openrouter_data)
    result = kulturpool_search(keywords_all)
    if result:
        return result

    #print("No results.")
    return None
