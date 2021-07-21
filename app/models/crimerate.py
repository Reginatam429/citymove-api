from app import db

class Crimerate(db.Model):
    crimerate_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    city_id = db.Column(db.Integer, db.ForeignKey('city.city_id'), nullable=True)
    crime_index = db.Column(db.Integer)
    safety_index = db.Column(db.Integer)