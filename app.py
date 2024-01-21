from flask import Flask
from flask_cors import CORS
from os import urandom
from plan import plan
 
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}) # means every route
app.secret_key = urandom(24).hex()

from plan import plan
app.register_blueprint(plan, url_prefix="/")

if __name__ == "__main__":
    app.run(debug=True)