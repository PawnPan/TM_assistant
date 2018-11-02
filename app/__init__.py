from flask import Flask, render_template, jsonify
import requests


app = Flask(__name__)


@app.route("/")
@app.route("/index")
def render_index():
    return render_template("index.html")


@app.route("/get_menu")
def get_menu():
    r = requests.get("https://www.ele.me/restapi/shopping/v2/menu?restaurant_id=854602&terminal=web")
    return jsonify(success=1, data=r.json())
