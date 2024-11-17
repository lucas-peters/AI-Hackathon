from app import create_app
import os
import sys
dir = os.path.dirname(os.path.abspath(__file__))
dir + '../../backend'
sys.path.append(dir)

app = create_app()
if __name__ == "__main__":
    app.run(debug=True)