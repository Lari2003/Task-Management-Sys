import json
import os

def load_data(filepath):
    """Load JSON data from a file."""
    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            return json.load(file)
    return []

def save_data(filepath, data):
    """Save data to a JSON file."""
    try:
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Data saved successfully to {filepath}.")
    except Exception as e:
        print(f"Error saving data to {filepath}: {e}")
