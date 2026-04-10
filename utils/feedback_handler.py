import json
import os

FEEDBACK_FILE = "data/feedback.json"

def save_feedback(entry):
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, "r") as f:
            # data = json.load(f)
            try:
                data = json.load(f) # prevent crash
            except:
                data = []
    else:
        data = []

    # Add new feedback
    if entry not in data:
        data.append(entry) # no duplicate

    with open(FEEDBACK_FILE, "w") as f: #write
        json.dump(data, f, indent=4)