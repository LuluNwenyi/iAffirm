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