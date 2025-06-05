from flask import Blueprint, render_template, session, redirect, url_for
from app.models.booking import booking1
from app.models.event import event1
from app.models.user import user1
from app import db

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin")
def admin_dashboard():
    if "user_email" not in session or session.get("user_email") != "admin@admin.com":
        return redirect(url_for("auth.login"))

    reservations = booking1.query.all()
    data = []
    for r in reservations:
        utilisateur = user1.query.get(r.utilisateur_id)
        evenement = event1.query.get(r.evenement_id)
        if utilisateur and evenement:
            data.append({
                "nom": utilisateur.nom,
                "email": utilisateur.email,
                "titre": evenement.titre,
                "date": evenement.date,
                "status": "Confirmé"
            })
    return render_template("admin_dashboard.html", reservations=data)
