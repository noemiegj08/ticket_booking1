from app import db, bcrypt

class user1(db.Model):
    __tablename__ = "user1"

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    mot_de_passe_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, mot_de_passe):
        self.mot_de_passe_hash = bcrypt.generate_password_hash(mot_de_passe).decode("utf-8")

    def verifier_password(self, mot_de_passe):
        return bcrypt.check_password_hash(self.mot_de_passe_hash, mot_de_passe)
