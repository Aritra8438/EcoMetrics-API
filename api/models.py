from .database import db


class Population(db.Model):
    # def __init__(self, _country, _year, _population):
    #     self.country = _country
    #     self.year = _year
    #     self.population = _population
    __tablename__ = "population"
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(100))
    year = db.Column(db.Integer)
    population = db.Column(db.BigInteger)
