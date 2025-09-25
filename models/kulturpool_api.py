import requests

# Base URL for Kulturpool API
BASE_URL = "https://api.kulturpool.at"

# your API function
def kulturpool_main(item):
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

# description

def kulturpool_search(extracted):
    kulturpool_main()
    # loop over person_names
    for person in extracted['person_names']:
        kulturpool_main(person)

    # loop over place_names
    for place in extracted['place_names']:
        kulturpool_main(place)

    # optional: loop over years (but may be noisy)
    for year in extracted['dates']:
        kulturpool_main(year)


# request
kulturpool_main("Helmker was a wealthy man with links to the Huosi, and Störmer 1984, p. 664, was of the opinion he belonged to the Huosi, himself. It is generally assumed that Helmker was trying to establish a small monastery in Singenbach. He endowed the church dedicated to St. Peter that he had built there with generous property in Singenbach, Ried, Walkertshofen and Pleitmannswang (TF 118), and also gave himself to the church, and then conveyed it to the bishopric of Freising (TF 119). Helmker had a son, named Rekinhoh, who is mentioned in TF 119.")