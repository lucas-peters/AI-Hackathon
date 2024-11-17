from flask import Blueprint, request, redirect, url_for, send_from_directory, make_response, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
from .s3_queries import get_password, create_user
import json

auth = Blueprint('auth', __name__)
@auth.route('/login', methods=["POST"])
def login():
    req = request.get_json()
    pass_hash = get_password(req['email'])
    
    if check_password_hash(pass_hash, req['password']):
        print("Login Successful!")
        return get_token(req['email'])
    else:
        print("Incorrect login")
    return jsonify({"msg": "Bad username or password"}), 401

@auth.route('/create_account', methods=['POST'])
def create_account():
    req = request.get_json()
    
    if not create_user(req):
        return jsonify({"msg": "Email Already Exists"}), 400
    return get_token(req['email'])


def get_token(email): # returns access token
    access_token = create_access_token(identity=email)
    # Set the JWT as a cookie
    return jsonify(access_token=access_token), 200