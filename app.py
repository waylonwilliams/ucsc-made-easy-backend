from flask import Flask
from flask_cors import CORS
from os import urandom, getuid
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String
from planner import db
from routes import bp


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})
app.secret_key = urandom(24).hex()

# app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{app.root_path}/data/planner.db"
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///planner.db"
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
