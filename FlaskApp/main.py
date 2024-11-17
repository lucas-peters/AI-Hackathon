from app import create_app
import os
import sys
dir = os.path.dirname(os.path.abspath(__file__))
dir + '../../backend'
sys.path.append(dir)
from app.chat import test_process_flask_request

app = create_app()
if __name__ == "__main__":
    #app.run(debug=True)
    json_obj = test_process_flask_request("I'm going to the Beach",'bob_gmail_com',{'time': '12:00:00', 'date': '12-24-2024'})
    print(json_obj)