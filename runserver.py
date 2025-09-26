from flask import Flask, render_template
from flask_caching import Cache
import re
from models.openrouter import openrouter_call
from models.thanados_api import get_thanados_data
from models.kulturpool_api import kulturpool_main
from models.get_relevant import  get_relevant

app = Flask(__name__)
app.config['CACHE_TYPE'] = 'FileSystemCache'
app.config['CACHE_DIR'] = '/var/tmp/flask-cache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 3600
cache = Cache(app)


@app.route("/")
def index():
    return render_template("index.html")


def extract_localized_text(text, preferred_lang="de"):
    # Regex patterns for each language
    patterns = {
        "de": r"##de_##(.*?)##_de##",
        "en": r"##en_##(.*?)##_en##"
    }

    # Try preferred language first
    match = re.search(patterns.get(preferred_lang, ""), text, re.DOTALL)
    if match:
        return match.group(1).strip()

    # Fallback to English if available
    if preferred_lang != "en":
        match = re.search(patterns["en"], text, re.DOTALL)
        if match:
            return match.group(1).strip()

    # Fallback: return original text
    return text.strip()


@app.route("/<int:id_>")
@cache.cached(timeout=120)
def entity_view(id_: int):
    data = get_thanados_data(id_)

    description = ''
    if data['description']:
        description = extract_localized_text(data['description'])
        data['description'] = description

    name = data['title']
    main_type = ''
    if data['types'] and data['types'][0]['isStandard']:
        main_type = data['types'][0]['title']


    base_url = "https://api.kulturpool.at/search"
    params = {
        "q": name + " " + main_type,
        "per_page": 250,
    }


    relv = get_relevant(name, description)
    openrouter = openrouter_call(description)
    kp_descrip_result, kp_keyall_result, kp_title_result, kp_person, kp_place = kulturpool_main(description, openrouter, name)

    relv_ids = {item["id"] for item in relv}  # make a set for fast lookup

    all_others = kp_descrip_result + kp_keyall_result + kp_title_result
    unique_by_id = list({item["id"]: item for item in all_others}.values())

    # Filter out items whose id is already in relv
    unique_by_id = [item for item in unique_by_id if item["id"] not in relv_ids]
    kp_person = [item for sublist in kp_person.values() for item in sublist[:5]]
    kp_person = list({item["id"]: item for item in kp_person}.values())

    kp_place = [item for sublist in kp_place.values() for item in sublist[:5]]
    kp_place = list({item["id"]: item for item in kp_place}.values())
    return render_template("entity_view.html", data=data, relv=relv, titledata=unique_by_id, rel_persons=kp_person, rel_places= kp_place)

@app.route("/openrouter/<id_>")
def openrouter_view(id_: int):
    data = get_thanados_data(id_)

    external_references = data['externalReferenceSystems']
    description = data['description']
    title = data['title']
    dates = data['when']
    types = [type_['title'] for type_ in data['types']]
    openrouter = openrouter_call(description)
    kp_descrip_result, kp_keyall_result, kp_title_result, kp_person, kp_place = kulturpool_main(description, openrouter, title)
    relv = get_relevant(title, description)

    return render_template(
        "openrouter_view.html",
        external_references=external_references,
        description=description,
        title=title,
        dates=dates,
        types=types,
        openrouter=openrouter)

if __name__ == "__main__":
    app.run(debug=True)
