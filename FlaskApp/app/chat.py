from flask import Blueprint, request, redirect, url_for, send_from_directory
from .s3_queries import get_location, make_key_string
import os
import sys
dir = os.path.dirname(os.path.abspath(__file__))
dir + '../../backend'
sys.path.append(dir)
from ...backend.prompt_processor import process_flask_request
import json

chat = Blueprint('views', __name__)

@chat.route('/')
def home(methods = ['GET', 'POST']):
    # check if user is logged_in
    # if not, redirect to login page
    if request.method == 'POST':
        json_req = request.get_json()
        req = json.loads(json_req)
        
        process_flask_request(req)
    
    if request.method == 'GET':
        pass
        
    #return render_template('../../frontend/src/app.html')
    return send_from_directory('client/public', 'app.html')