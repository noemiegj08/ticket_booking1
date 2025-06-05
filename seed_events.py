from app import create_app, db
from app.models.event import event1
from datetime import datetime

app = create_app()

with app.app_context():
    e1 = event1(titre="Festival Lumière", date=datetime(2025, 8, 15), capacite=150, prix=35.0)
    e2 = event1(titre="Concert des Étoiles", date=datetime(2025, 9, 1), capacite=200, prix=40.0)
    
    db.session.add_all([e1, e2])
    db.session.commit()

    print("Événements insérés avec succès.")
