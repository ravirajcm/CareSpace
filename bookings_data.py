import pandas as pd
import threading

CSV_FILE = 'bookings.csv'
LOCK = threading.Lock()

COLUMNS = [
    'Space ID', 'Name', 'Duration (hours)', 'Date',
    'Start Timestamp', 'End Timestamp'
]

def load_bookings():
    with LOCK:
        try:
            df = pd.read_csv(CSV_FILE, dtype=str)
        except FileNotFoundError:
            df = pd.DataFrame(columns=COLUMNS)
    return df

def save_bookings(df):
    with LOCK:
        df.to_csv(CSV_FILE, index=False)
