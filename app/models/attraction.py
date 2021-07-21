from app import db

class Attraction(db.Model):
    attraction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    city_id = db.Column(db.Integer, db.ForeignKey('city.city_id'),
    nullable=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    image_url = db.Column(db.String)