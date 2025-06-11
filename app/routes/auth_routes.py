from flask import Blueprint, render_template, request, redirect, url_for, make_response, current_app
from app.models.user import user1
import jwt
import datetime
from app import db

auth_bp = Blueprint("auth", __name__)

# Route inscription
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

# Route connexion
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        mot_de_passe = request.form["password"]

        utilisateur = user1.query.filter_by(email=email).first()

        if utilisateur and utilisateur.verifier_password(mot_de_passe):
            payload = {
                "nom": utilisateur.nom,
                "email": utilisateur.email,
                "role": utilisateur.role,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }
            token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")

            resp = make_response(redirect(url_for("auth.redirect_dashboard")))
            resp.set_cookie("jwt", token, httponly=True)
            return resp

        return render_template("login.html", message="Identifiants incorrects")

    return render_template("login.html")

# Redirection selon le rôle
@auth_bp.route("/redirect_dashboard")
def redirect_dashboard():
    token = request.cookies.get("jwt")
    if not token:
        return redirect(url_for("auth.login"))

    try:
        data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        if data["role"] == "admin":
            return redirect(url_for("admin.admin_dashboard"))
        else:
            return redirect(url_for("auth.dashboard"))
    except jwt.ExpiredSignatureError:
        return redirect(url_for("auth.login"))
    except jwt.InvalidTokenError:
        return redirect(url_for("auth.login"))

# Dashboard utilisateur normal
@auth_bp.route("/dashboard")
def dashboard():
    token = request.cookies.get("jwt")
    if not token:
        return redirect(url_for("auth.login"))

    try:
        data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        return render_template("dashboard.html", utilisateur=data)
    except:
        return redirect(url_for("auth.login"))

# Déconnexion
@auth_bp.route("/logout")
def logout():
    resp = make_response(redirect(url_for("auth.login")))
    resp.set_cookie("jwt", "", expires=0)
    return resp



