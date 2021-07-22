from flask import Blueprint, request, jsonify, make_response
from app import db
from .models.city import City
from .models.col import Col
from .models.crimerate import Crimerate
from .models.attraction import Attraction
from dotenv import load_dotenv
# example_bp = Blueprint('example_bp', __name__)
load_dotenv()

cities_bp = Blueprint("cities", __name__, url_prefix="/cities")
cols_bp = Blueprint("cols", __name__, url_prefix="/cols")
crimerates_bp = Blueprint("crimerates", __name__, url_prefix="/crimerates")
attractions_bp = Blueprint("attractions", __name__, url_prefix="/attractions")

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

# Get all crimerate belonging to one city by ID
@cities_bp.route("/<city_id>/crimerates", methods=["GET"])
def get_all_crimerate_by_city(city_id):
    city = City.query.get(city_id)
    if city is None:
        return make_response("", 404)

    if request.method == "GET":
        crimerates = Crimerate.query.filter(Crimerate.city_id == city_id).order_by(Crimerate.crimerate_id.desc())
        results = []
        for crimerate in crimerates:
            print("~~~~~~~~~~~~~~~", crimerate.crimerate_id)
            results.append({
                "crimerate_id": crimerate.crimerate_id,
                "city_id": crimerate.city_id,
                "crime_index": crimerate.crime_index,
                "safety_index": crimerate.safety_index  
            })

        return make_response(
                {
                    "city_id": city.city_id,
                    "city_name": city.city_name,
                    "crimerate": results
                }, 200)

# Get all attractions belonging to one city by ID
@cities_bp.route("/<city_id>/attractions", methods=["GET"])
def get_all_attraction_by_city(city_id):
    city = City.query.get(city_id)
    if city is None:
        return make_response("", 404)

    if request.method == "GET":
        attractions = Attraction.query.filter(Attraction.city_id == city_id).order_by(Attraction.attraction_id.desc())
        results = []
        for attraction in attractions:
            print("~~~~~~~~~~~~~~~", attraction.attraction_id)
            results.append({
                "attraction_id": attraction.attraction_id,
                "city_id": attraction.city_id,
                "name": attraction.name,
                "description": attraction.description,
                "image_url": attraction.image_url,  
            })

        return make_response(
                {
                    "city_id": city.city_id,
                    "city_name": city.city_name,
                    "attraction": results
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
                    "city_id": col.city_id,
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

#~~~~~~~~~~~~~~~~~~~crimerate endpoints~~~~~~~~~~~~~~~~~~~
# Create crimerate | Get all crimerates
@crimerates_bp.route("", methods=["POST", "GET"])
def handle_crimerates():
        if request.method == "GET":
            crimerates = Crimerate.query.all()
            crimerates_response = []
            for crimerate in crimerates:
                crimerates_response.append({
                    "crimerate_id": crimerate.crimerate_id,
                    "city_id": crimerate.city_id,
                    "crime_index": crimerate.crime_index,
                    "safety_index": crimerate.safety_index
                })
            return jsonify(crimerates_response, 200)

        elif request.method == "POST":
            request_body = request.get_json()

            if 'city_id' not in request_body or 'crime_index' not in request_body or 'safety_index' not in request_body:
                return {"details": "Invalid data"}, 400
            new_crimerate = Crimerate(
                            city_id=request_body["city_id"],
                            crime_index=request_body["crime_index"],
                            safety_index=request_body["safety_index"]
                            )

            db.session.add(new_crimerate)
            db.session.commit()

            return {
                "city": {
                    "crimerate_id": new_crimerate.crimerate_id,
                    "city_id": new_crimerate.city_id,
                    "crime_index": new_crimerate.crime_index,
                    "safety_index": new_crimerate.safety_index
                }
            }, 201

# Get crimerate by ID | Delete crimerate by ID | Edit crimerate by ID
@crimerates_bp.route("/<crimerate_id>", methods=["GET", "DELETE", "PUT"])
def handle_crimerate(crimerate_id):
    crimerate = Crimerate.query.get(crimerate_id)
    if crimerate is None:
        return make_response("", 404)

    if request.method == "GET":
        return {
                "crimerate_id": crimerate.crimerate_id,
                "city_id": crimerate.city_id,
                "crime_index": crimerate.crime_index,
                "safety_index": crimerate.safety_index
            }
    elif request.method == "DELETE":
        message = {"details": f"Crimerate {crimerate.crimerate_id} \" from City id: {crimerate.city_id}\" successfully deleted"}
        db.session.delete(crimerate)
        db.session.commit()
        return make_response(message)
    elif request.method == "PUT":
        form_data = request.get_json()
        print("form data", form_data )

        crimerate.city_id = form_data["city_id"]
        crimerate.crime_index = form_data["crime_index"]
        crimerate.safety_index = form_data["safety_index"]

        db.session.commit()

        return make_response({
                "crimerate": {
                    "crimerate_id": crimerate.crimerate_id,
                    "city_id": crimerate.city_id,
                    "crime_index": crimerate.crime_index,
                    "safety_index": crimerate.safety_index
                }
        })

#~~~~~~~~~~~~~~~~~~~attraction endpoints~~~~~~~~~~~~~~~~~~~
# Create attraction | Get all attractions
@attractions_bp.route("", methods=["POST", "GET"])
def handle_attractions():
        if request.method == "GET":
            attractions = Attraction.query.all()
            attractions_response = []
            for attraction in attractions:
                attractions_response.append({
                    "attraction_id": attraction.attraction_id,
                    "city_id": attraction.city_id,
                    "name": attraction.name,
                    "description": attraction.description,
                    "image_url": attraction.image_url
                })
            return jsonify(attractions_response, 200)

        elif request.method == "POST":
            request_body = request.get_json()

            if 'city_id' not in request_body or 'name' not in request_body or 'description' not in request_body or 'image_url' not in request_body:
                return {"details": "Invalid data"}, 400
            new_attraction = Attraction(
                            city_id=request_body["city_id"],
                            name=request_body["name"],
                            description=request_body["description"],
                            image_url=request_body["image_url"]
                            )

            db.session.add(new_attraction)
            db.session.commit()

            return {
                "attraction": {
                    "attraction_id": new_attraction.attraction_id,
                    "city_id": new_attraction.city_id,
                    "name": new_attraction.name,
                    "description": new_attraction.description,
                    "image_url": new_attraction.image_url
                }
            }, 201

# Get attraction by ID | Delete attraction by ID | Edit attraction by ID
@attractions_bp.route("/<attraction_id>", methods=["GET", "DELETE", "PUT"])
def handle_attraction(attraction_id):
    attraction = Attraction.query.get(attraction_id)
    if attraction is None:
        return make_response("", 404)

    if request.method == "GET":
        return {
                "attraction_id": attraction.attraction_id,
                "city_id": attraction.city_id,
                "name": attraction.name,
                "description": attraction.description,
                "image_url": attraction.image_url
            }
    elif request.method == "DELETE":
        message = {"details": f"Attraction {attraction.attraction_id} \" from City id: {attraction.city_id}\" successfully deleted"}
        db.session.delete(attraction)
        db.session.commit()
        return make_response(message)
    elif request.method == "PUT":
        form_data = request.get_json()
        print("form data", form_data )

        attraction.city_id = form_data["city_id"]
        attraction.name = form_data["name"]
        attraction.description = form_data["description"]
        attraction.image_url = form_data["image_url"]

        db.session.commit()

        return make_response({
                "attraction": {
                    "attraction_id": attraction.attraction_id,
                    "city_id": attraction.city_id,
                    "name": attraction.name,
                    "description": attraction.description,
                    "image_url": attraction.image_url
                }
        })