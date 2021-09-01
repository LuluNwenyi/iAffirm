##############################
######### IMPORTS ############
##############################

from api import db

# AFFiRMATION TABLE
class Affirmation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String)

    def to_json(self):
        return {"text": self.text}

    db.create_all()



# ADMiN TABLE
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    email = db.Column(db.String)
    admin = db.Column(db.Boolean)

    def to_json(self):
        return {"username": self.username, "email": self.email}

    db.create_all()



# TOKEN BLOCKLiST TABLE
class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    db.create_all()
