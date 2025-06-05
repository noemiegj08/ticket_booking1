from app.models.booking import booking1
from app.models.event import event1
from flask import render_template, redirect, url_for, session
from flask import Blueprint, render_template, request, redirect, session
from app.models.user import user1
from app import db


auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nom = request.form["nom"]
        email = request.form["email"]
        mot_de_passe = request.form["password"]

        nouvel_utilisateur = user1(nom=nom, email=email)
        nouvel_utilisateur.set_password(mot_de_passe)
        db.session.add(nouvel_utilisateur)
        db.session.commit()

        return render_template("login.html", message="Inscription réussie !")

    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        mot_de_passe = request.form["password"]

        utilisateur = user1.query.filter_by(email=email).first()

        
        if utilisateur and utilisateur.verifier_password(mot_de_passe):
            session["user_nom"] = utilisateur.nom
            session["user_email"] = utilisateur.email
            return redirect(url_for("auth.dashboard"))

        return render_template("login.html", message="Identifiants incorrects")

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@auth_bp.route("/dashboard")
def dashboard():
    if "user_email" not in session:
        return redirect(url_for("auth.login"))

    utilisateur = user1.query.filter_by(email=session["user_email"]).first()
    reservations = booking1.query.filter_by(utilisateur_id=utilisateur.id).all()

    evenements_reserves = []
    for reservation in reservations:
        evenement = event1.query.get(reservation.evenement_id)
        if evenement:
            evenements_reserves.append(evenement)

    return render_template("dashboard.html", utilisateur=utilisateur, evenements=evenements_reserves)

