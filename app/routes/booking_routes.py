from flask import Blueprint, render_template, request, redirect, url_for, session
from app import db
from app.models.booking import booking1
from app.models.event import event1
from app.models.user import user1

booking_bp = Blueprint("booking", __name__)

@booking_bp.route("/reserver/<int:event_id>", methods=["GET", "POST"])
def reserver(event_id):
    # Vérifie si l'utilisateur est connecté
    if "user_email" not in session or "user_nom" not in session:
        return render_template("unauthorized.html")

    # Récupère l'événement demandé
    evenement = event1.query.get(event_id)

    if not evenement:
        return render_template("message.html", message="Événement inexistant."), 404

    if evenement.capacite <= 0:
        return render_template("message.html", message="Événement complet."), 400

    if request.method == "POST":
        numero = request.form.get("numero_carte")
        expiration = request.form.get("expiration")
        cvv = request.form.get("cvv")

        if not (numero and expiration and cvv):
            return render_template("booking.html", evenement=evenement, erreur="Tous les champs sont requis")

        # DEBUG : Affiche l'email utilisé pour retrouver l'utilisateur
        print("Email utilisé pour trouver l'utilisateur :", session.get("user_email"))

        utilisateur = user1.query.filter_by(email=session["user_email"]).first()
        if not utilisateur:
            print("⚠️ Aucun utilisateur trouvé avec cet email.")
            return render_template("message.html", message="Utilisateur introuvable."), 404

        # Crée la réservation liée à l'utilisateur connecté
        reservation = booking1(
            utilisateur_id=utilisateur.id,
            evenement_id=evenement.id
        )
        evenement.capacite -= 1
        db.session.add(reservation)
        db.session.commit()

        return render_template("message.html", message="Réservation confirmée pour l'événement")

    # Affiche le formulaire si la méthode est GET
    return render_template("booking.html", evenement=evenement)




