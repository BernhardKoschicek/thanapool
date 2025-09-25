import requests
import re

# Base URL for Kulturpool API
url = "https://api.kulturpool.at/search"

def kulturpool_search(name):
    """
    function that calls kulturpool api and queries the database for param: item
    returns result as dict
    """
    number_of_results = find_number_of_results(name)
    print(f'Number of results found: {number_of_results}')

    info_dict = dict()
    for i in range(1, number_of_results // 20 + 2):
        data = get_data_of_page(name, i)
        for hit in data['hits']:
            doc = hit['document']
            info_dict[doc['id']] = [doc['title'][0], doc['previewImage'], doc['isShownAt']]
    res_list = []
    for k in info_dict.keys():
        d = {}
        d['id'] = k
        d['title'] = info_dict[k][0]
        d['previewImage'] = info_dict[k][1]
        d['isShownAt'] = info_dict[k][2]
        res_list.append(d)
    return res_list

def find_number_of_results(name):
    params = {
        'q': name,
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data["found"]

def get_data_of_page(name, page):
    params = {
        'q': name,
        'page': page
    }
    response = requests.get(url, params=params)
    return response.json()

def description_text(description):
    """Function to clean up the description if there is a description in German and in English."""
    match = re.search(r"##de_##(.*?)##_de##", description, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()

def kulturpool_search_extended(openrouter_data):
    """Function to loop through all categories provided in the dictionary from openrouter."""
    keys = ['person_names', 'entity_names', 'place_names', 'dates', 'taxonomic_subject',
            'typological_subject', 'actions']
    for i in keys:
        for j in openrouter_data[i]:
            category_results = kulturpool_search(j)
            return category_results

def extract_keywords(openrouter_data):
    """Function that extracts the keywords from the openrouter dictionary
    and joins them to one long string to query.
    """
    keywords = []
    for values in openrouter_data.values():
        keywords.extend(values)
    keywords_all = " ".join(keywords)
    return keywords_all

def kulturpool_main(description, openrouter_data, title):
    """Function that calls the search function to query Kulturpool with
    a) the description and
    b) the all keywords.
    parameters: description and the openrouter dictionary.
    returns the result dictionary from the queries. """
    # get description and try query with description
    descrip = description_text(description)
    result_descrip = kulturpool_search(descrip)
    # get keywords and try with all keywords
    keywords_all = extract_keywords(openrouter_data)
    result_keyall = kulturpool_search(keywords_all)
    # query with title
    result_title = kulturpool_search(title)
    # specific for each category
    result_keyspec = kulturpool_search_extended(openrouter_data)
    return result_descrip, result_keyall, result_title, result_keyspec

