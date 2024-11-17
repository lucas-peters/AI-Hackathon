from flask import Blueprint, render_template, request, flash, redirect, url_for, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from .s3_queries import get_password, get_location, make_key_string
import json

views = Blueprint('views', __name__)

@views.route('/')
def home():
    if request.form == 'POST':
        # need to tweek these based on frontend
        if location is None:
            location = get_location()
        if time and date are null:
            #get datetime
            pass
        #key_string = make_key_string(user)
        #tdl = {'location' : location, 'date': date, 'time' : time, 'prompt': prompt, 'user_id': key_string}
        #json_data = json.dumps(tdl)
        
        #shanaya_func(json_data)
        
        
        # receive time/date/location from frontend
        # if any are null, I fill them in
        # pack into json 
        # send user_id, json, raw_promt to Shanaya
        # wait for response??
        
    #return render_template('../../frontend/src/app.html')
    return send_from_directory('client/public', 'app.html')
    

@views.route('/login', methods=['GET', "POST"])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password1')
        pass_hash = get_password(email)
        if check_password_hash(pass_hash, password):
            print("Login Successful!")
            return redirect(url_for('views.home'))
        else:
            print("Incorrect login")
    return send_from_directory('client/public', 'login.html')


@views.route('/create_account')
def create_account():
    pass
"""
    if request.method == 'POST':
        if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')"""
        