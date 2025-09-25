from flask import Flask, render_template

from models.openrouter import openrouter_call
from models.thanados_api import get_thanados_data

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/<id_>")
def entity_view(id_: int):
    print(id_)

    data = get_thanados_data(id_)

    external_references = data['externalReferenceSystems']
    description = data['description']
    title = data['title']
    dates = data['when']
    types = data['types']
    openrouter=openrouter_call()
    return render_template("entity_view.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
