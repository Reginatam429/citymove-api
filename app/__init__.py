from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# import os

db = SQLAlchemy()
migrate = Migrate()
# load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    #     "SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://postgres:postgres@localhost:5432/citymove_api"

    db.init_app(app)
    migrate.init_app(app, db)

    from app.models.city import City
    from app.models.col import Col
    from app.models.crimerate import Crimerate
    from app.models.attraction import Attraction

        # Endpoints
    from .routes import hello_world_bp
    app.register_blueprint(hello_world_bp)

    return app