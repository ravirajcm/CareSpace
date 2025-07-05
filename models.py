from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from db import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    specialization = db.Column(db.String(80), nullable=False)
    position = db.Column(db.String(80), nullable=False)
    reservations = db.relationship('Reservation', backref='user', lazy=True)

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    type = db.Column(db.String(80), nullable=False)  # e.g., Lab, Office, Consultation Room
    reservations = db.relationship('Reservation', backref='resource', lazy=True)

    @staticmethod
    def match_resource(action, user_id):
        # Simple matching logic based on action
        # Extend with user history/routine as needed
        if action == 'Lab work':
            return Resource.query.filter_by(type='Lab').first()
        elif action == 'Patient consultation':
            return Resource.query.filter_by(type='Consultation Room').first()
        elif action == 'Research':
            return Resource.query.filter_by(type='Office').first()
        return None

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    resource_id = db.Column(db.Integer, db.ForeignKey('resource.id'), nullable=False)
    time_slot = db.Column(db.String(80), nullable=False)  # e.g., '2025-07-05 14:00-16:00'
    status = db.Column(db.String(20), nullable=False)  # pending, confirmed, cancelled

    @staticmethod
    def check_conflict(resource_id, time_slot):
        # Simple conflict check: does resource have a reservation at this time?
        return Reservation.query.filter_by(resource_id=resource_id, time_slot=time_slot, status='confirmed').first() is not None
