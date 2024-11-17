from flask import Blueprint, request, redirect, url_for, send_from_directory, make_response, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
from .s3_queries import get_password, create_user
from flask_login import login_required
from . import login_manager
from user import User
import json

auth = Blueprint('auth', __name__)
@auth.route('/login', methods=["POST"])
def login():
    json_req = request.get_json()
    req = json.loads(json_req)

    pass_hash = get_password(req['email'])
    
    if check_password_hash(pass_hash, req['password']):
        print("Login Successful!")
        return get_token(req['email'])
    else:
        print("Incorrect login")
    return jsonify({"msg": "Bad username or password"}), 401

@auth.route('/create_account')
def create_account(methods=['POST']):
    json_req = request.get_json()
    req = json.loads(json_req)
    
    if not create_user(req):
        return jsonify({"msg": "Email Already Exists"}), 400
    return get_token(req['email'])


def get_token(email): # returns access token
    access_token = create_access_token(identity=email)
    # Set the JWT as a cookie
    return jsonify(access_token=access_token), 200