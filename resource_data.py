import csv
import threading

CSV_FILE = 'resources.csv'
LOCK = threading.Lock()

# In-memory cache of resources (list of dicts)
_resources = []

FIELDS = [
    'Space ID', 'OfficeName', 'Category', 'Area (sqm)',
    'Capacity (people)', 'Specialized Equipment', 'Conference Equip.', 'Bookable'
]

def load_resources():
    global _resources
    with LOCK:
        with open(CSV_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            _resources = list(reader)
    return _resources

def get_resources():
    if not _resources:
        load_resources()
    return _resources

def add_resource(resource):
    with LOCK:
        _resources.append(resource)
        save_resources()

def update_resource(space_id, new_data):
    with LOCK:
        for i, r in enumerate(_resources):
            if r['Space ID'] == space_id:
                _resources[i].update(new_data)
                save_resources()
                return True
    return False

def save_resources():
    with LOCK:
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(_resources)

def find_resource_by_action(action):
    # Dummy matching logic: match Category or Equipment
    for r in get_resources():
        if action.lower() in r['Category'].lower() or action.lower() in r['Specialized Equipment'].lower():
            return r
    return None

def check_conflict(resource_id, time_needed):
    # Placeholder: always return False (no conflict)
    return False
