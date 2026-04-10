import json
import os

FEEDBACK_FILE = "data/feedback.json"

def save_feedback(entry):
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []

    # Add new feedback
    data.append(entry)

    with open(FEEDBACK_FILE, "w") as f: #write
        json.dump(data, f, indent=4)