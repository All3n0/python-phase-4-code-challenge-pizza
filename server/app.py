#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"
@app.route("/restaurants")
def get_restaurants():
    restaurants=[]
    for restaurant in Restaurant.query.all():
        restaurants.append(restaurant.to_dict(rules=["-restaurant_pizzas"]))
    return make_response(restaurants, 200)

@app.route("/restaurants/<int:id>", methods=["GET", "DELETE"])
def restaurant(id):
    restaurant = Restaurant.query.filter_by(id=id).first()
    if request.method == "GET":
        if not restaurant:
            return make_response({"error": "Restaurant not found"}, 404)
        return make_response(restaurant.to_dict(), 200)
    if request.method == "DELETE": 
        if not restaurant:
            return make_response({"error": "Restaurant not found"}, 404)
        db.session.delete(restaurant)
        db.session.commit()
        return make_response(restaurant.to_dict(), 204)
    
@app.route("/pizzas")
def get_pizzas():
    pizzas=[]
    for pizza in Pizza.query.all():
        pizzas.append(pizza.to_dict(rules=["-restaurant_pizzas"]))
    return make_response(pizzas, 200)
@app.route("/restaurant_pizzas", methods=["POST"])
def create_restaurant_pizza():
    data = request.json
    try:
        rp = RestaurantPizza(price=data.get('price'), restaurant_id=data.get('restaurant_id'), pizza_id=data.get('pizza_id'))
        db.session.add(rp)
        db.session.commit()
        return rp.to_dict(), 201
    except Exception as e:
        print(e)
        return {'errors':["validation errors"]}, 400


if __name__ == "__main__":
    app.run(port=5555, debug=True)
