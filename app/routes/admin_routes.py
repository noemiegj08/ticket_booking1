from flask import Blueprint, render_template, request, redirect, url_for, current_app
import jwt
from app.models.user import user1
from app.models.event import event1

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin_dashboard")
def admin_dashboard():
    from app.models.booking import booking1  # ⬅️ ici, l'import est déplacé **dans** la fonction

    token = request.cookies.get("jwt")

    if not token:
        return redirect(url_for("auth.login"))

    try:
        data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])

        if data["role"] != "admin":
            return redirect(url_for("auth.login"))

        reservations = booking1.query.all()
        tableau = []

        for r in reservations:
            utilisateur = user1.query.get(r.utilisateur_id)
            evenement = event1.query.get(r.evenement_id)
            tableau.append({
                "utilisateur": utilisateur.nom if utilisateur else "Inconnu",
                "email": utilisateur.email if utilisateur else "Inconnu",
                "evenement": evenement.titre if evenement else "Inconnu",
                "date": r.date_reservation,
                "statut": r.statut
            })

        return render_template("admin_dashboard.html", reservations=tableau)

    except jwt.ExpiredSignatureError:
        return redirect(url_for("auth.login"))
    except jwt.InvalidTokenError:
        return redirect(url_for("auth.login"))
