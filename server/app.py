#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

# GET /bakeries: returns a list of JSON objects for all bakeries
@app.route('/bakeries')
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(jsonify(bakeries), 200)

# GET /bakeries/<int:id>: returns a single bakery as JSON
@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()
    if bakery is None:
        return make_response(jsonify({"error": "Bakery not found"}), 404)
    bakery_serialized = bakery.to_dict()
    return make_response(jsonify(bakery_serialized), 200)

# POST /baked_goods: creates a new baked good in the database
@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    data = request.form
    new_baked_good = BakedGood(
        name=data['name'],
        price=data['price'],
        bakery_id=data.get('bakery_id')  # optional, if a bakery_id is provided
    )
    db.session.add(new_baked_good)
    db.session.commit()
    
    return make_response(jsonify(new_baked_good.to_dict()), 201)

# PATCH /bakeries/<int:id>: updates the name of the bakery
@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    bakery = Bakery.query.filter_by(id=id).first()
    if bakery is None:
        return make_response(jsonify({"error": "Bakery not found"}), 404)
    
    data = request.form
    if 'name' in data:
        bakery.name = data['name']
    
    db.session.commit()
    return make_response(jsonify(bakery.to_dict()), 200)

# DELETE /baked_goods/<int:id>: deletes a baked good from the database
@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.filter_by(id=id).first()
    if baked_good is None:
        return make_response(jsonify({"error": "Baked good not found"}), 404)
    
    db.session.delete(baked_good)
    db.session.commit()
    return make_response(jsonify({"message": "Baked good successfully deleted"}), 200)

# GET /baked_goods/by_price: returns a list of baked goods sorted by price in descending order
@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_by_price_serialized = [bg.to_dict() for bg in baked_goods_by_price]
    return make_response(jsonify(baked_goods_by_price_serialized), 200)

# GET /baked_goods/most_expensive: returns the single most expensive baked good
@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if most_expensive is None:
        return make_response(jsonify({"error": "No baked goods found"}), 404)
    most_expensive_serialized = most_expensive.to_dict()
    return make_response(jsonify(most_expensive_serialized), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
