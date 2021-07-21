from flask import Blueprint, request, jsonify, make_response
from app import db
from .models.city import City
from dotenv import load_dotenv
# example_bp = Blueprint('example_bp', __name__)
load_dotenv()

hello_world_bp = Blueprint("hello_world", __name__)
cities_bp = Blueprint("cities", __name__, url_prefix="/cities")

@hello_world_bp.route("/hello-world", methods=["GET"])
def say_hello_world():
    my_response_body = "Hello, World!"
    return my_response_body

#~~~~~~~~~~~~~~~~~~~city endpoints~~~~~~~~~~~~~~~~~~~
# Create City | Get all cities
@cities_bp.route("", methods=["POST", "GET"])
def handle_cities():
    if request.method == "GET":
        cities = City.query.all()
        cities_response = []
        for city in cities:
            cities_response.append({
                "city_id": city.city_id,
                "city_name": city.city_name,
                "city_state": city.city_state
            })
        return jsonify(cities_response, 200)

    elif request.method == "POST":
        request_body = request.get_json()

        if 'city_name' not in request_body or 'city_state' not in request_body:
            return {"details": "Invalid data"}, 400
        new_city = City(
            city_name=request_body["city_name"],
            city_state=request_body["city_state"]                
        )

        db.session.add(new_city)
        db.session.commit()

    return {
        "city": {
            "city_id": new_city.city_id,
            "city_name": new_city.city_name,
            "city_state": new_city.city_state
        }
    }, 201

# Get city by ID | Delete city by ID | Edit city by ID
@cities_bp.route("/<city_id>", methods=["GET", "DELETE", "PUT"])
def handle_city(city_id):
    city = City.query.get(city_id)
    if city is None:
        return make_response("", 404)

    if request.method == "GET":
        return {
                "city_id": city.city_id,
                "city_name": city.city_name,
                "city_state": city.city_state
            }
    elif request.method == "DELETE":
        message = {"details": f"City {city.city_id} \"{city.city_name}\" successfully deleted"}
        db.session.delete(city)
        db.session.commit()
        return make_response(message)
    elif request.method == "PUT":
        form_data = request.get_json()
        print("form data", form_data )

        city.city_name = form_data["city_name"]
        city.city_state = form_data["city_state"]

        db.session.commit()

        return make_response({
                "city": {
                    "city_id": city.city_id,
                    "city_name": city.city_name,
                    "city_state": city.city_state,
                }
        })

#~~~~~~~~~~~~~~~~~~~col endpoints~~~~~~~~~~~~~~~~~~~