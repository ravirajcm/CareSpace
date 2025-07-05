# Testing the Hospital Reservation System

This guide explains how to test the hospital reservation system, including setup, running the app, and verifying its core features.

## 1. Setup

**a. Clone or navigate to the project directory:**
```
# Clone the repository
git clone git@github.com:ravirajcm/CareSpace.git
cd CareSpace
```

**b. Create and activate a virtual environment:**
```
python3 -m venv venv
source venv/bin/activate
```

**c. Install dependencies:**
```
pip install -r requirements.txt
```

## 2. Run the Backend Server

Start the Flask backend:
```
python app.py
```
- By default, the server runs at [http://127.0.0.1:8001](http://127.0.0.1:8001)

## 3. Access the Frontend

Open your web browser and go to:
```
http://127.0.0.1:8001/
```

## 4. Test the User Flow

1. **Start the chat**: The web UI will prompt for your username.
2. **Enter details**: Provide your specialization and position (e.g., Doctor, Nurse).
3. **Specify activity**: State what you need to do (Lab work, Patient consultation, Research).
4. **Specify time**: Enter the time you need the space (e.g., `2025-07-05 14:00-16:00`).
5. **Confirm booking**: The agent will propose a resource. Type `Yes` to confirm or `No` to cancel.
6. **Repeat or restart**: You may start a new booking after confirming or cancelling.

## 5. Additional Testing Tips

- Try different roles and activities to see how the agent responds.
- Try overlapping bookings to test conflict detection.
- Check the terminal for backend errors or logs.

---

For advanced or automated testing, consider using tools like Postman for API endpoints or writing unit tests. If you need help with this, let us know!
