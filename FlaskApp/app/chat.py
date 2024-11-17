from flask import Blueprint, request, redirect, url_for, send_from_directory
from .s3_queries import get_location, make_key_string
import os
import sys
dir = os.path.dirname(os.path.abspath(__file__))
dir + '../../backend'
sys.path.append(dir)
from s3_queries import make_key_string
from backend.prompt_processor import process_flask_request
import json

chat = Blueprint('views', __name__)
model_return = {}

@chat.route('/')
def home(methods = ['GET', 'POST']):
    # check if user is logged_in
    # if not, redirect to login page
    if request.method == 'POST':
        req = request.get_json()
        user_id = make_key_string(req['email'])
        prompt = req['prompt']
        req.pop('prompt', None)
        req.pop('email', None)
        model_return = process_flask_request(prompt, user_id, req)
        return model_return[1].json_dumps()
    
    if request.method == 'GET':
        pass
        
    #return render_template('../../frontend/src/app.html')
    

def test_process_flask_request(prompt, user_id, req):
    return process_flask_request(prompt,user_id, req)