import pandas as pd
import threading

CSV_FILE = 'spaces.csv'
LOCK = threading.Lock()

COLUMNS = [
    'Space ID', 'OfficeName', 'Category', 'Area (sqm)',
    'Capacity (people)', 'Specialized Equipment', 'Conference Equip.', 'Bookable'
]

def load_spaces():
    with LOCK:
        try:
            df = pd.read_csv(CSV_FILE, dtype=str)
        except FileNotFoundError:
            df = pd.DataFrame(columns=COLUMNS)
    return df

def save_spaces(df):
    with LOCK:
        df.to_csv(CSV_FILE, index=False)
