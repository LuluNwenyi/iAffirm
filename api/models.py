##############################
######### IMPORTS ############
##############################

from api import db

#########################################
########## AFFIRMATION TABLE ############
#########################################

class Affirmation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String)

    def to_json(self):
        return {"text": self.text}

    db.create_all()