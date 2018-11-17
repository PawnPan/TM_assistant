from flask import Flask, render_template, jsonify, request
import requests
from settings import config
from pymongo import MongoClient
import time
import datetime
from functools import wraps


db_cli = MongoClient(config.MONGODB_HOST)
db = db_cli[config.MONGODB_NAME]


app = Flask(__name__)


class OrderError(Exception):
    pass


def error_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except OrderError as e:
            return jsonify(success=0, msg=str(e))

    return wrapper


@app.route("/")
@app.route("/index")
def render_index():
    return render_template("index.html")


@app.route("/get_menu")
def get_menu():
    r = requests.get("https://www.ele.me/restapi/shopping/v2/menu?restaurant_id=854602&terminal=web")
    return jsonify(success=1, data=r.json())


@app.route('/order', methods=["POST"])
@error_handler
def order():
    meat_name = request.values.get("meat_name")
    vege_name = request.values.get("vege_name")
    person_name = request.values.get("person_name")
    price = request.values.get("price")

    if not person_name:
        raise OrderError("你是谁呀")

    if not vege_name:
        if meat_name:
            raise OrderError("木有点素菜，你要只吃肉嘛")
        else:
            raise OrderError("不要什么都不点就来调戏我")

    order = {
        "vege_name": vege_name,
        "person_name": person_name,
        "price": price,
        "order_time": datetime.datetime.now(),
        "order_type": 1,
        "_id": int(time.time())
    }
    if meat_name:
        order.update(
            meat_name=meat_name,
            order_type=2,
        )
    db.orders.save(order)
    return jsonify(success=1, data=order)


@app.route("/get_orders")
def get_orders():
    tmp_dttime = datetime.datetime.now() + datetime.timedelta(hours=6)
    tmp_begin_time = datetime.datetime(tmp_dttime.year, tmp_dttime.month, tmp_dttime.day, 0, 0, 0)\
                     + datetime.timedelta(hours=-6)
    tmp_end_time = datetime.datetime(tmp_dttime.year, tmp_dttime.month, tmp_dttime.day, 23, 59, 59)\
                   + datetime.timedelta(hours=-6)
    query = {
        "order_time": {
            "$gt": tmp_begin_time,
            "$lt": tmp_end_time,
        }
    }
    orders = list(db.orders.find(query))
    return jsonify(success=1, data=orders)
