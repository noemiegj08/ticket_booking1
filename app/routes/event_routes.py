from flask import Blueprint, render_template, request, redirect, jsonify
from app.models.event import event1
from app import db

event_bp = Blueprint("event", __name__)

# API JSON (optionnelle)
@event_bp.route("/events", methods=["GET"])
def get_events():
    events = event1.query.all()
    return jsonify([
        {
            "id": e.id,
            "titre": e.titre,
            "date": e.date.strftime("%Y-%m-%d"),
            "prix": e.prix
        } for e in events
    ])

# Page HTML avec tous les événements
@event_bp.route("/evenements")
def afficher_evenements():
    events = event1.query.all()
    return render_template("evenements.html", events=events)

# 🆕 Page d'accueil
@event_bp.route("/")
def accueil():
    events = event1.query.all()
    return render_template("index.html", events=events)
