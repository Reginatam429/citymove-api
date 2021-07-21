from app import db

class Col(db.Model):
    col_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    city_id = db.Column(db.Integer, db.ForeignKey('city.city_id'), nullable=True)
    milk_cost = db.Column(db.DECIMAL(asdecimal=False))
    transport_ticket = db.Column(db.DECIMAL(asdecimal=False))
    gas = db.Column(db.DECIMAL(asdecimal=False))
    basic_utilities = db.Column(db.DECIMAL(asdecimal=False))
    rent = db.Column(db.DECIMAL(asdecimal=False))
    avg_monthly_salary = db.Column(db.DECIMAL(asdecimal=False))