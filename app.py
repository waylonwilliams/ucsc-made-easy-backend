from flask import Flask
from flask_cors import CORS
import os
from planner import db
from routes import bp


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})
app.secret_key = os.urandom(24).hex()

if not os.path.exists("data"):
    os.makedirs("data")
file_path = os.path.join("data", "planner.db")
if not os.path.exists( file_path ):
    with open(file_path, 'w') as f:
        pass


# file_path = path.abspath(getcwd())+"/database.db"
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:////{app.root_path}/data/planner.db"
# app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///data/planner.db"
# app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///planner.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.teardown_appcontext
def close_connection(exception):
    db.session.remove()

app.register_blueprint(bp)

if __name__ == "__main__":
    app.run(debug=True)
