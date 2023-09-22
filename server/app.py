#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response,abort
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        plant_list = [
            {
                "id": plant.id,
                "name": plant.name,
                "image": plant.image,
                "price": float(plant.price)  # Convert Decimal to float for JSON
            }
            for plant in plants
        ]
        response = make_response(jsonify(plant_list))
        return response
api.add_resource(Plants, '/plants')

class PlantByID(Resource):
    def get(self, plant_id):
        plant = Plant.query.get(plant_id)

        if not plant:
            return abort(404, message="Plant not found")

        plant_data = {
            "id": plant.id,
            "name": plant.name,
            "image": plant.image,
            "price": float(plant.price)  # Convert Decimal to float for JSON
        }

        response = make_response(jsonify(plant_data))
        return response
api.add_resource(PlantByID, '/plants/<int:plant_id>')       

if __name__ == '__main__':
    app.run(port=5555, debug=True)
