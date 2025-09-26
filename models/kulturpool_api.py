import re
from models.get_relevant import find_number_of_results, get_data_of_page

def kulturpool_search(name, n = 100):
    """
    Gets query response from find_number_of_results.
    :param name: query string
    :param n: number of results wanted
    :return res_list: list of dictionaries, one per result, containing id, title, previewImage, and isShownAt
    """
    number_of_results = find_number_of_results(name)
    print(f'Number of results found: {number_of_results}')

    info_dict = dict()
    for i in range(1, min(number_of_results, n) // 20 + 2):
        data = get_data_of_page(name, i)
        for hit in data['hits']:
            doc = hit['document']
            if 'previewImage' in doc.keys():
                info_dict[doc['id']] = [doc['title'][0], doc['previewImage'], doc['isShownAt']]
            else:
                info_dict[doc['id']] = [doc['title'][0], '', doc['isShownAt']]
    res_list = []
    for k in info_dict.keys():
        d = {}
        d['id'] = k
        d['title'] = info_dict[k][0]
        d['previewImage'] = info_dict[k][1]
        d['isShownAt'] = info_dict[k][2]
        res_list.append(d)
    return res_list


def description_text(description):
    """
    Gets the description from Thanados and cleans the description if there is a German and English description.
    :param description: description from object in Thanados
    :return description: returns the cleaned or if no action necessary, the original description
    """



    # 1. Replace newlines/tabs with spaces
    description = re.sub(r'[\r\n\t]+', ' ', description)

    # 2. Remove any characters that are not letters, numbers, punctuation, or spaces
    description = re.sub(r"[^a-zA-Z0-9äöüÄÖÜß.,;:!?'\-\(\)\[\] ]+", "", description)

    # 3. Collapse multiple spaces into one
    description = re.sub(r'\s+', ' ', description).strip()



    match = re.search(r"##de_##(.*?)##_de##", description, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    else:
        return description

def kulturpool_search_extended(openrouter_data, categories = None):
    """
    Gets the results from openrouter.py.
    Queries the Kulturpool (with kulturpool_search function) for each keyword for specified categories, provided by openrouter.
    :param openrouter_data: dictionary of keywords for multiple categories
    :param categories: default is person_names and place_names
    :return category_results: list of the results from the queries for each keyword for the specified categories
    """
    if categories is None:
        categories = ["person_names", "place_names"]

    all_results = {}

    for category in categories:
        if category in openrouter_data:
            all_results[category] = {}
            for keyword in openrouter_data[category]:
                all_results[category][keyword] = kulturpool_search(keyword)

    pers_results = all_results.get("person_names", {})
    plac_results = all_results.get("place_names", {})

    return pers_results, plac_results


def extract_keywords(openrouter_data):
    """
    Gets the keyword dictionary from openrouter.py and extracts each keyword.
    The keywords are then joined to use as a query.
    :param openrouter_data: dictionary of keywords for multiple categorised
    :return keywords_all: str, all keywords from openrouter joined together
    """
    keywords = []
    for values in openrouter_data.values():
        keywords.extend(values)
    keywords_all = " ".join(keywords)
    return keywords_all

def kulturpool_main(description, openrouter_data, title):
    """
    Run Kulturpool queries using the description from Thanados, the keywords from openrouter as one string,
    the title from Thanados,and category-specific keywords from openrouter.
    :param description: str, free-text description from Thanados
    :param openrouter_data: dict, keywords grouped by categories
    :param title: str, title string from Thanados
    :return: returns the lists result_descrip, result_keyall, result_title, person_result, place_result
    """
    # get description and try query with description
    descrip = description_text(description)
    result_keyall = []
    result_descrip = []
    if description != '':
        result_descrip = kulturpool_search(descrip)

        keywords_all = extract_keywords(openrouter_data)

        print('keywords_all')
        print(keywords_all)
        if keywords_all != '':
            result_keyall = kulturpool_search(keywords_all)
    # get keywords and try with all keywords

    # query with title
    result_title = kulturpool_search(title)
    # for specified categories (person and place)
    person_result, place_result = kulturpool_search_extended(openrouter_data)
    return result_title, result_descrip, result_keyall, person_result, place_result

