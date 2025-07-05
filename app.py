from flask import Flask, request, jsonify, session
from db import db
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db.init_app(app)

from models import User, Reservation
import resource_data

@app.before_request
def before_request_func():
    if not hasattr(app, 'db_initialized'):
        db.create_all()
        app.db_initialized = True

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    user = User(
        username=data['username'],
        specialization=data['specialization'],
        position=data['position']
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered', 'user_id': user.id})

@app.route('/start_booking', methods=['POST'])
def start_booking():
    data = request.json
    user_id = data['user_id']
    action = data['action']  # Lab work, Patient consultation, Research
    time_needed = data['time_needed']
    # TODO: Add user history/routine logic
    # Find available resource using resource_data
    resource = resource_data.find_resource_by_action(action)
    if not resource:
        return jsonify({'message': 'No available resource found'}), 404
    # Check for conflicts (dummy for now)
    if resource_data.check_conflict(resource['Space ID'], time_needed):
        return jsonify({'message': 'Conflict detected, cannot book'}), 409
    # Create reservation (pending confirmation)
    # NOTE: resource_id is now resource['Space ID'], resource_name is resource['OfficeName']
    reservation = Reservation(
        user_id=user_id,
        resource_id=resource['Space ID'],
        time_slot=time_needed,
        status='pending'
    )
    db.session.add(reservation)
    db.session.commit()
    return jsonify({'message': 'Reservation pending confirmation', 'reservation_id': reservation.id, 'resource': resource['OfficeName']})

@app.route('/confirm_booking', methods=['POST'])
def confirm_booking():
    data = request.json
    reservation_id = data['reservation_id']
    agree = data['agree']
    reservation = Reservation.query.get(reservation_id)
    if not reservation:
        return jsonify({'message': 'Reservation not found'}), 404
    if agree:
        reservation.status = 'confirmed'
        db.session.commit()
        return jsonify({'message': 'Booking confirmed'})
    else:
        db.session.delete(reservation)
        db.session.commit()
        return jsonify({'message': 'Booking cancelled'})

from flask import send_from_directory

@app.route('/')
def serve_index():
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('frontend', path)

if __name__ == '__main__':
    app.run(debug=True, port=8001)
