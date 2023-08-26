from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = SQLAlchemy()

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    password = db.Column(db.LargeBinary)
    ruolo = db.Column(db.Enum('analyst', 'admin', 'specialist', 'developer', name ='ruoli'))
    disponibilità = db.Column(db.Boolean)
    score = db.Column(db.Integer)
    

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password,
            "ruolo": self.ruolo,
            "disponibilità": self.disponibilità,
            "score": self.score
        }