from .database import db


class Population(db.Model):
    __tablename__ = "population"
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(100))
    year = db.Column(db.Integer)
    population = db.Column(db.BigInteger)


class GDPperCapita(db.Model):
    __tablename__ = "gdp_per_capita"
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(100))
    year = db.Column(db.Integer)
    gdp_per_capita = db.Column(db.Numeric)
