from app import db



class booking1(db.Model):
    __tablename__ = "booking1"

    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey("user1.id"), nullable=False)
    evenement_id = db.Column(db.Integer, db.ForeignKey("event1.id"), nullable=False)
    statut = db.Column(db.String(20), default="confirmé", nullable=False)
    paiement_status = db.Column(db.String(20), default="en attente")
