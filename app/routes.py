from flask import Blueprint, request, jsonify, make_response
from app import db
from .models.city import City
from .models.col import Col
from dotenv import load_dotenv
# example_bp = Blueprint('example_bp', __name__)
load_dotenv()

hello_world_bp = Blueprint("hello_world", __name__)
cities_bp = Blueprint("cities", __name__, url_prefix="/cities")
cols_bp = Blueprint("cols", __name__, url_prefix="/cols")
# crimerates_bp = Blueprint("crimerates", __name__, url_prefix="/crimerates")
# attractions_bp = Blueprint("attractions", __name__, url_prefix="/attractions")

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

#~~~~~~~~~~~~~~~~~~~City relationship endpoints~~~~~~~~~~~~~~~~~~~
# Get all COL belonging to one city by ID
@cities_bp.route("/<city_id>/cols", methods=["GET"])
def get_all_col_by_city(city_id):
    city = City.query.get(city_id)
    if city is None:
        return make_response("", 404)

    if request.method == "GET":
        cols = Col.query.filter(Col.city_id == city_id).order_by(Col.col_id.desc())
        results = []
        for col in cols:
            print("~~~~~~~~~~~~~~~", col.col_id)
            results.append({
                "col_id": col.col_id,
                "city_id": col.city_id,
                "milk_cost": col.milk_cost,
                "transport_ticket": col.transport_ticket,
                "gas": col.gas,
                "basic_utilities": col.basic_utilities,
                "rent": col.rent,
                "avg_monthly_salary": col.avg_monthly_salary
                
            })

        return make_response(
                {
                    "city_id": city.city_id,
                    "city_name": city.city_name,
                    "col": results
                }, 200)

#~~~~~~~~~~~~~~~~~~~col endpoints~~~~~~~~~~~~~~~~~~~
# Create col | Get all cols
@cols_bp.route("", methods=["POST", "GET"])
def handle_cols():
        if request.method == "GET":
            cols = Col.query.all()
            cols_response = []
            for col in cols:
                cols_response.append({
                    "col_id": col.col_id,
                    "city_id": city.city_id,
                    "milk_cost": col.milk_cost,
                    "transport_ticket": col.transport_ticket,
                    "gas": col.gas,
                    "basic_utilities": col.basic_utilities,
                    "rent": col.rent,
                    "avg_monthly_salary": col.avg_monthly_salary
                })
            return jsonify(cols_response, 200)

        elif request.method == "POST":
            request_body = request.get_json()

            if 'city_id' not in request_body or 'milk_cost' not in request_body or 'transport_ticket' not in request_body or 'gas' not in request_body or 'basic_utilities' not in request_body or 'rent' not in request_body or 'avg_monthly_salary' not in request_body:
                return {"details": "Invalid data"}, 400
            new_col = Col(
                            city_id=request_body["city_id"],
                            milk_cost=request_body["milk_cost"],
                            transport_ticket=request_body["transport_ticket"],
                            gas=request_body["gas"],
                            basic_utilities=request_body["basic_utilities"],
                            rent=request_body["rent"],
                            avg_monthly_salary=request_body["avg_monthly_salary"])

            db.session.add(new_col)
            db.session.commit()

            return {
                "city": {
                    "col_id": new_col.col_id,
                    "city_id": new_col.city_id,
                    "milk_cost": new_col.milk_cost,
                    "transport_ticket": new_col.transport_ticket,
                    "gas": new_col.gas,
                    "basic_utilities": new_col.basic_utilities,
                    "rent": new_col.rent,
                    "avg_monthly_salary": new_col.avg_monthly_salary
                }
            }, 201

# Get col by ID | Delete col by ID | Edit col by ID
@cols_bp.route("/<col_id>", methods=["GET", "DELETE", "PUT"])
def handle_col(col_id):
    col = Col.query.get(col_id)
    if col is None:
        return make_response("", 404)

    if request.method == "GET":
        return {
                "col_id": col.col_id,
                "city_id": col.city_id,
                "milk_cost": col.milk_cost,
                "transport_ticket": col.transport_ticket,
                "gas": col.gas,
                "basic_utilities": col.basic_utilities,
                "rent": col.rent,
                "avg_monthly_salary": col.avg_monthly_salary
            }
    elif request.method == "DELETE":
        message = {"details": f"COL {col.col_id} \" from City id: {col.city_id}\" successfully deleted"}
        db.session.delete(col)
        db.session.commit()
        return make_response(message)
    elif request.method == "PUT":
        form_data = request.get_json()
        print("form data", form_data )

        col.city_id = form_data["city_id"]
        col.milk_cost = form_data["milk_cost"]
        col.transport_ticket = form_data["transport_ticket"]
        col.gas = form_data["gas"]
        col.basic_utilities = form_data["basic_utilities"]
        col.rent = form_data["rent"]
        col.avg_monthly_salary = form_data["avg_monthly_salary"]

        db.session.commit()

        return make_response({
                "col": {
                    "col_id": col.col_id,
                    "city_id": col.city_id,
                    "milk_cost": col.milk_cost,
                    "transport_ticket": col.transport_ticket,
                    "gas": col.gas,
                    "basic_utilities": col.basic_utilities,
                    "rent": col.rent,
                    "avg_monthly_salary": col.avg_monthly_salary
                }
        })