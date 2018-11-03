from flask import Flask, render_template, jsonify
import requests
from settings import config
from pymongo import MongoClient


db_cli = MongoClient(config.MONGODB_HOST)
db = db_cli[config.MONGODB_NAME]


app = Flask(__name__)


@app.route("/")
@app.route("/index")
def render_index():
    return render_template("index.html")


@app.route("/get_menu")
def get_menu():
    r = requests.get("https://www.ele.me/restapi/shopping/v2/menu?restaurant_id=854602&terminal=web")
    return jsonify(success=1, data=r.json())
