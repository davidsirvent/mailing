from . import db

class Config(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_address = db.Column(db.String(100))
    password = db.Column(db.String(100))
    smtp_server = db.Column(db.String(100))
    smtp_port = db.Column(db.Integer)