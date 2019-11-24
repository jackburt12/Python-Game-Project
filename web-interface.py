import player
from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/")
def index():
    if player is None:
        return render_template("create-character.html")
    else:
        return render_template("game-interface.html")
