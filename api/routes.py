##############################
######### IMPORTS ############
##############################

from api.decorators import admin_required
from flask_jwt_extended import jwt_required
from api.models import Affirmation
from flask import Blueprint, jsonify, request
from api import db

main = Blueprint('main', __name__)


# INDEX PAGE
@main.route('/')
def index():
    return jsonify({'message': 'Welcome to the iAffirm API'})



# CREATE AFFIRMATION
@main.route('/affirmation', methods=['POST'])
def create_affirmation():

    text = request.json['text']

    new_affirmation = Affirmation(text=text)

    db.session.add(new_affirmation)
    db.session.commit()

    return jsonify({'message': 'Affirmation added!'})



# GET ALL AFFIRMATIONS
@main.route('/affirmations', methods=['GET'])
def get_affirmations():

    affirmations = Affirmation.query.all()

    all_affirmations = []
    for affirmation in affirmations:
        affirmation_data = {}
        affirmation_data['text_id'] = affirmation.id
        affirmation_data['text'] = affirmation.text

        all_affirmations.append(affirmation_data)

    return jsonify({'affirmations': all_affirmations})




# GET ONE AFFIRMATION
@main.route('/affirmation/<id>', methods=['GET'])
def get_one_affirmations(id):

    affirmation = Affirmation.query.filter_by(id=id).first()

    if not affirmation:
        return jsonify({'message': "No affirmation found!"})

    affirmation_data = {}
    affirmation_data['text_id'] = affirmation.id
    affirmation_data['text'] = affirmation.text

    return jsonify({'affirmation': affirmation_data})



# EDIT AN AFFIRMATION 
@main.route('/affirmation/<id>', methods=['PUT'])
@jwt_required()
@admin_required
def edit_affirmation(id):

    affirmation = Affirmation.query.filter_by(id=id).first()

    if affirmation:

        try:

            text = request.json['text']
            
            affirmation.text = text   

            db.session.commit()

            return jsonify("Affirmation updated successfully!")

        except Exception as e:
            # IF NO ERROR OCCURS...
            response = {
                "message": str (e)
            }
            return jsonify(response)

    else:
        # IF THERE IS NO SUCH MESSAGE, GIVE:
        response = {
            'message' : 'This affirmation does not exist.'
        }
        return jsonify(response)



# DELETE AN AFFIRMATION
@main.route('/affirmation/<id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_affirmation(id):

    affirmation = Affirmation.query.filter_by(id=id).first()

    if affirmation:


        db.session.delete(affirmation)
        db.session.commit()

        response = {
            "message" : "You have deleted this affirmation message successfully!"
            }

        return jsonify(response)

    else:
        response = {
                    'message' : 'This affirmation does not exist.'
                    }

        return jsonify(response)
