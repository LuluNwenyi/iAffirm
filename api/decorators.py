##############################
######### IMPORTS ############
##############################
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from functools import wraps
from .models import User

# ADMIN DECORATOR
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user = get_jwt_identity()
        user = User.query.filter_by(admin=True, username=current_user).first()
        if not user:
            return jsonify({'message': 'You are not an admin!'}), 401
        return f(*args, **kwargs)
    return decorated_function