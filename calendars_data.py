import pandas as pd
import threading

CSV_FILE = 'calendars.csv'
LOCK = threading.Lock()

COLUMNS = [
    'Doctor_Id', 'Date', 'Day', 'Time', 'Activity', 'Location', 'Notes'
]

def load_calendars():
    with LOCK:
        try:
            df = pd.read_csv(CSV_FILE, dtype=str)
        except FileNotFoundError:
            df = pd.DataFrame(columns=COLUMNS)
    return df

def save_calendars(df):
    with LOCK:
        df.to_csv(CSV_FILE, index=False)
