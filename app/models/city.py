from app import db

class City(db.Model):
    city_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    city_name = db.Column(db.String)
    state = db.Column(db.String)