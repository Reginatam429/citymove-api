from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")

    db.init_app(app)
    migrate.init_app(app, db)

    CORS(app)
    from app.models.city import City
    from app.models.col import Col
    from app.models.crimerate import Crimerate
    from app.models.attraction import Attraction

    # Endpoints
    # Register Blueprints here
    # from .routes import example_bp
    from .routes import hello_world_bp
    from .routes import cities_bp
    from .routes import cols_bp
    from .routes import crimerates_bp
    # from .routes import attractions_bp
    app.register_blueprint(hello_world_bp)
    app.register_blueprint(cities_bp)
    app.register_blueprint(cols_bp)
    app.register_blueprint(crimerates_bp)
    # app.register_blueprint(attractions_bp)

    return app