from flask import Blueprint, request, redirect, url_for, send_from_directory, make_response, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
from .s3_queries import get_password, create_user
from flask_login import login_required
from . import login_manager
from user import User

auth = Blueprint('auth', __name__)
@auth.route('/login', methods=["POST"])
def login():
    email = request.form.get('email')
    password = request.form.get('password1')
    pass_hash = get_password(email)
    
    if check_password_hash(pass_hash, password):
        print("Login Successful!")
        return get_token(email)
    else:
        print("Incorrect login")
    return jsonify({"msg": "Bad username or password"}), 401

@auth.route('/create_account')
def create_account(methods=['POST']):
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password1')
    age = request.form.get('age')
    gender = request.form.get('gender')
    location = request.form.get('location')
    if not create_user(name, email, password1, age, gender, location):
        return jsonify({"msg": "Email Already Exists"}), 400
    return get_token(email)


def get_token(email): # returns access token
    access_token = create_access_token(identity=email)
    # Set the JWT as a cookie
    return jsonify(access_token=access_token), 200