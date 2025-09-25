from flask import Flask, render_template
import requests

from models.openrouter import openrouter_call
from models.thanados_api import get_thanados_data
from models.kulturpool_api import kulturpool_main

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/<id_>")
def entity_view(id_: int):
    print(id_)

    data = get_thanados_data(id_)
    name = data['title']
    main_type = ''
    if data['types'] and data['types'][0]['isStandard']:
        main_type = data['types'][0]['title']


    base_url = "https://api.kulturpool.at/search"
    params = {
        "q": name + " " + main_type,
        "per_page": 250,
    }




    try:
        kp_response = requests.get(base_url, params=params, timeout=10)
        kp_response.raise_for_status()
        kp_data = kp_response.json()
    except requests.RequestException as e:
        print(f"Fehler bei API-Request: {e}")
        kp_data = {"found": 0, "hits": []}

    return render_template("entity_view.html", data=data, kp_data=kp_data)

@app.route("/openrouter/<id_>")
def openrouter_view(id_: int):
    data = get_thanados_data(id_)

    external_references = data['externalReferenceSystems']
    description = data['description']
    title = data['title']
    dates = data['when']
    types = [type_['title'] for type_ in data['types']]
    openrouter = openrouter_call(description)
    kulturpool_result = kulturpool_main(description, openrouter)
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
