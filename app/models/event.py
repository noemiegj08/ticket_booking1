from app import db


class event1(db.Model):
    __tablename__ = "event1"  

    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    capacite = db.Column(db.Integer, nullable=False)
    prix = db.Column(db.Float, nullable=False)

