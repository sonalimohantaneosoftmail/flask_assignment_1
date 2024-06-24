# from flask import Blueprint, request, jsonify
# from app.models import User
# from app import db , bcrypt
# # from app.utils.jwt import create_access_token
# from flask_jwt_extended import create_access_token,create_refresh_token, jwt_required, get_jwt_identity
# # from flask_bcrypt import Bcrypt

# bp = Blueprint('auth', __name__, url_prefix='/auth')
# # bcrypt = Bcrypt()

# @bp.route('/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
#     new_user = User(name=data['username'], email=data['email'], password=hashed_password)
#     db.session.add(new_user)
#     db.session.commit()
#     return jsonify({"message": "User registered successfully!"}), 201

# @bp.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     user = User.query.filter_by(email=data['email']).first()
#     if user and bcrypt.check_password_hash(user.password, data['password']):
#         access_token = create_access_token(identity={'id': user.id, 'email': user.email})
#         return jsonify({"access_token": access_token}), 200
#     else:
#         return jsonify({"message": "Invalid credentials!"}), 401



# @bp.route('/refresh', methods=['POST'])
# @jwt_required(refresh=True)
# def refresh():
#     identity = get_jwt_identity()
#     access_token = create_access_token(identity=identity)
#     return jsonify(access_token=access_token), 200



from flask import Blueprint, request, jsonify
from app import db, bcrypt
from app.models import User
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

main_data = Blueprint('auth', __name__, url_prefix='/auth')

@main_data.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(name=data['username'], email=data['email'], password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify(message="User registered successfully"), 201

@main_data.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity={'id': user.id, 'name': user.name, 'email': user.email})
        refresh_token = create_refresh_token(identity={'id': user.id, 'name': user.name, 'email': user.email})
        return jsonify(access_token=access_token, refresh_token=refresh_token), 200
    return jsonify(message="Invalid credentials"), 401

@main_data.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token), 200
