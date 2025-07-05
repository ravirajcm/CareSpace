import pandas as pd
import threading

CSV_FILE = 'doctors.csv'
LOCK = threading.Lock()

COLUMNS = [
    'DoctorID', 'Specialty', 'DoctorName', 'Email',
    'Dedicated Space in Office', 'Office Id', 'Home Office'
]

def load_doctors():
    with LOCK:
        try:
            df = pd.read_csv(CSV_FILE, dtype=str)
        except FileNotFoundError:
            df = pd.DataFrame(columns=COLUMNS)
    return df

def save_doctors(df):
    with LOCK:
        df.to_csv(CSV_FILE, index=False)
