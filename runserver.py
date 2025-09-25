from flask import Flask, render_template

from models.openrouter import openrouter_call

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", openrouter=openrouter_call())

@app.route("/<id_: int>")
def entity_view(id_: int):
    data = {
        "id": 196314,
        "title": "The Novara sails from Sydney to Auckland",
        "description": {
            "en": "On 7 December 1858, the Novara departed Sydney and set sail for Auckland...",
            "de": "Am 7. Dezember 1858 verließ die Novara Sydney und segelte nach Auckland..."
        },
        "start_date": "1858-12-07",
        "end_date": "1858-12-22",
        "media": [
            {"title": "Auckland 1858/1859", "url": "/static/img/auckland.jpg"},
            {"title": "Sydney 1858", "url": "/static/img/sydney.jpg"},
            {"title": "Route map", "url": "/static/img/route.jpg"}
        ],
        "participants": [
            {"name": "Bernhard von Wüllerstorf-Urbair", "role": "Expedition Leader"},
            {"name": "Ferdinand von Hochstetter", "role": "Geologist"},
            {"name": "Carl Scherzer", "role": "Scientist"}
        ],
        "related_events": [
            {"title": "The Novara stays in Sydney", "url": "#"},
            {"title": "The Novara sails from Auckland to Tahiti", "url": "#"}
        ]
    }
    return render_template("entity_view.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
