from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:password@localhost/booking_db"
app.config["SECRET_KEY"] = "45hKgfd8!#ZrxzYYkq29dmLqpwW"

db = SQLAlchemy(app)

class user1(db.Model):
    __tablename__ = 'user1'  
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    mot_de_passe_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="user")

with app.app_context():
    utilisateur = user1.query.filter_by(email="noemie.gj08@gmail.com").first()
    if utilisateur:
        utilisateur.role = "admin"
        db.session.commit()
        print(f"{utilisateur.nom} a été promu administrateur.")
    else:
        print("Utilisateur non trouvé.")

