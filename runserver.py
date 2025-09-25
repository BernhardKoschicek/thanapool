from flask import Flask, render_template

from models.openrouter import openrouter_call

app = Flask(__name__)

@app.route("/")
def index():
    print(openrouter_call())
    return render_template("index.html", openrouter=openrouter_call())

if __name__ == "__main__":
    app.run(debug=True)
