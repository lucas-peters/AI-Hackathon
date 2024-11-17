from flask import Blueprint, request, redirect, url_for, send_from_directory
from .s3_queries import get_location, make_key_string
from . import login_manager
import json

views = Blueprint('views', __name__)

@views.route('/')
def home(methods = ['POST']):
    # check if user is logged_in
    # if not, redirect to login page
        
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