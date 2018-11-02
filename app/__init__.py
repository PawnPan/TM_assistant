from flask import Flask, render_template, request, jsonify


app = Flask(__name__)


@app.route("/")
@app.route("/index")
def render_index():
    return render_template("index.html")
