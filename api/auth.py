##############################
######### IMPORTS ############
##############################

from flask import Blueprint, jsonify, request, make_response, url_for, current_app, abort
from api import db, jwt, mail, ACCESS_EXPIRES
from .models import Admin, TokenBlocklist
from .decorators import admin_required
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message
import datetime

auth = Blueprint('auth', __name__)


# FUNCTION TO SEND MAIL
mail = Mail()
def send_email(to_email, subject, body):
  msg = Message(subject, recipients=[to_email])
  msg.html = body
  mail.send(msg)



# ADMiN SiGN UP ROUTE
@auth.route('/admin', methods=['POST'])
def create_admin():

    # QUERY IF ADMIN EXISTS
    admin = Admin.query.filter_by(email=request.json['email']).first()

    if not admin:

        try:
            # REGISTER THE USER
            username = request.json['username']
            email = request.json['email']
            password = request.json['password']
            password = generate_password_hash(password)

            new_admin = Admin(username=username, email=email, password=password, admin=True)

            db.session.add(new_admin)
            db.session.commit()

            response = {
                "message" : "You have registered this admin successfully!"
            }

            return jsonify(response), 201

        except Exception as e:
            # IF ERROR OCCURED...
            response = {
                "message": str (e)
            }
            return jsonify(response), 400

    else:
        # IF ADMIN ALREADY EXISTS
        response = {
            'message' : 'This admin already exists.'
        }
        return jsonify(response), 401



# LOGiN ROUTE
@auth.route('/login', methods=['POST'])
def login():

    # GET THE USER
    request_data = request.get_json()
    username = request_data['username']
    password = request_data['password']

    admin = Admin.query.filter_by(username=username).first()

    # IF NOT REGISTERED USER

    if not admin:
        return make_response('No user found', 401, {'WWW-Authenticate' : 'Basic realm= "Login required!"'})

    # TO CHECK IF PASSWORD IS CORRECT

    if admin and check_password_hash(admin.password, password):

        token = create_access_token(identity=username, expires_delta=ACCESS_EXPIRES)
        return jsonify({ 'token': token })

    return make_response('We could not verify this user', 401, {'WWW-Authenticate' : 'Basic realm = "Login required!"'})



# LOGOUT ROUTE
@auth.route('/logout', methods=['DELETE'])
@jwt_required()
def logout():

    # TO CHECK FOR THE TOKEN AND DELETE IT
    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(jwt_header, jwt_payload):
        jti = jwt_payload['jti']
        token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
        return token is not None


    # TO REMOVE THE TOKEN FROM THE DATABASE
    jti =get_jwt()['jti']
    now = datetime.datetime.utcnow()
    db.session.add(TokenBlocklist(jti=jti, created_at=now))
    db.session.commit()

    return jsonify({"message": "Successfully logged out"}), 200



# GET ALL ADMINS ROUTE
@auth.route('/admins', methods=['GET'])
@jwt_required()
@admin_required
def get_all_admins():

    # FiLTER USERS 
    admins = Admin.query.filter_by(admin=True).all()

    # RETURN ALL USERS
    pomodoroll_admins = []
    for admin in admins:
        pomodoroll_admin = {
            'username': admin.username,
            'email': admin.email,
            'id': admin.id,
        }
        pomodoroll_admins.append(pomodoroll_admin)
        
    return jsonify(pomodoroll_admins), 200



# GET USER BY ID ROUTE
@auth.route('/admin/<id>', methods=['GET'])
@jwt_required()
def get_user(id):

    # FiND ADMiN BY ID
    admin = Admin.query.filter_by(id=id).first()
    if not admin:
        return jsonify({'message': 'User not found!'}), 404

    admin = {
        'username': admin.username,
        'email': admin.email,
        'id': admin.id,
    }
    return jsonify(admin), 200



# EDiT ADMiN BY ID ROUTE
@auth.route('/admin/<id>', methods=['PUT'])
@jwt_required()
@admin_required
def edit_user(id):

    # FiND USER BY USER ID
    admin = Admin.query.filter_by(id=id).first()
    if not admin:
        return jsonify({'message': 'Admin not found!'}), 404
    
    # GET THE USER DATA
    if admin:

        try:

            username = request.json['username']
            email = request.json['email']

            admin.username = username
            admin.email = email

            db.session.commit()

            return jsonify("This admin's data has been updated successfully!"), 200

        except Exception as e:
            # IF ERROR OCCURED...
            response = {
                "message": str (e)
            }
            return jsonify(response), 400

    else:
        # IF USER DOESN'T EXIST
        response = {
            'message' : 'This admin does not exist.'
        }
        return jsonify(response), 404



# DELETE ADMiN BY ID ROUTE
@auth.route('/admin/<id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_user(id):
    
    # FiND ADMiN BY ID
    admin = Admin.query.filter_by(id=id).first()
    if not admin:
        return jsonify({'message': 'Admin not found!'}), 404

    # DELETE THE ADMiN
    db.session.delete(admin)
    db.session.commit()

    return jsonify({'message' : 'This admin has been deleted!'}), 200



# FORGOT PASSWORD ROUTE
@auth.route('/forgot-password', methods=['POST'])
def forgot_password():
    
    # GET THE DATA FROM THE REQUEST
    email = request.json['email']

    # CHECK IF USER EXISTS
    admin = Admin.query.filter_by(email=email).first()
    
    # IF USER EXISTS
    if admin:

        # GENERATE THE TOKEN
        subject = "Password Reset Link"
        ts = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        token = ts.dumps(email, salt='email-confirm-key')
        recover_url = url_for("auth.resetpassword", token=token,  _external=True)

        # SEND THE EMAIL
        text = f"Hi {admin.username}, Please reset " + \
              f"your password by clicking on the link: {recover_url} " + \
            f"If you didn't ask for a password reset, ignore the mail."

        send_email(to_email=admin.email, subject=subject, body=text)
        return jsonify({ "msg": "succesfully sent the reset mail to your email"}), 200 




# RESET PASSWORD ROUTE
@auth.route('/reset/<token>', methods=['PATCH'])
def resetpassword(token):

    ts = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])

    # GET THE DATA FROM THE REQUEST
    password = request.json['password']

    # CHECK FOR THE EMAIL AND TOKEN
    try:
        email = ts.loads(token, salt="email-confirm-key", max_age=86400)
    except:
        abort(404)

    if email is False:
        return jsonify({"message": "Invalid token or token expired"}), 401
    
    admin = Admin.query.filter_by(email=email).first()    
    if not admin:
        return jsonify({"message": "User not found"}), 404  

    # IF THE USER EXISTS 
    if admin:
        admin.password = generate_password_hash(password)
        db.session.commit()
        return jsonify({'message': 'Your password has been reset!'})

    else:
        return {"message": "An error occured"},   400