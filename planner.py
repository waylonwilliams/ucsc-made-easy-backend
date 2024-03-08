from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Planner(db.Model):
    __tablename__ = "planner"
    course_select_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_id = db.Column(db.String(36), nullable=True)
    position = db.Column(db.Integer, nullable=True)
    course = db.Column(db.String(60), nullable=True)
