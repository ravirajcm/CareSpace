# Hospital Reservation System

A simple agent-based hospital reservation system to book spaces for hospital staff based on their needs, position, and routine.

## Features
- User identification (username, specialization, position)
- Chat-based booking flow
- Resource/space matching
- Conflict detection
- Booking confirmation

## Project Structure
- `app.py` - Main backend API (Flask)
- `models.py` - Database models (User, Reservation, Resource)
- `database.db` - SQLite database
- `README.md` - Project documentation

## Setup
```bash
pip install -r requirements.txt
python app.py
```

## Usage
Visit the running web server and interact with the agent to book a space.
