from flask import Blueprint, request, redirect, url_for, send_from_directory
from .s3_queries import get_location, make_key
import os
import sys
dir = os.path.dirname(os.path.abspath(__file__))
dir + '../../backend'
sys.path.append(dir)
from backend.prompt_processor import process_flask_request
from flask_cors import cross_origin
import json

chat = Blueprint('views', __name__)
model_return = {}

@chat.route('/recommend', methods = ['POST'])
@cross_origin()
def home():
    # check if user is logged_in
    # if not, redirect to login page
    if request.method == 'POST':
        req = request.get_json()
        user_id = make_key(req['email'])
        prompt = req['prompt']
        req.pop('prompt', None)
        req.pop('email', None)
        print("XX:", prompt, user_id, req)
        model_return = process_flask_request(prompt, user_id, req)
        json_model_return_0 = json.loads(model_return[0])
        json_model_return_1 = json.loads(model_return[1])
        if type(json_model_return_0) == dict and type(json_model_return_1) == dict:
            json_data = {**json_model_return_0, **json_model_return_1}
        else:
            json_data = json_model_return_0
        return json_data
    
    if request.method == 'GET':
        pass
        
    #return render_template('../../frontend/src/app.html')
    

def test_process_flask_request(prompt, user_id, req):
    return process_flask_request(prompt,user_id, req)[0], process_flask_request(prompt,user_id, req)[1]