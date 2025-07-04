import json
from datetime import datetime
from config import LOG_FILE

screen_log = []

def log_action(activity_type, detail=""):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "activity": activity_type,
        "detail": detail
    }
    screen_log.append(entry)
    with open(LOG_FILE, "w") as f:
        json.dump(screen_log, f, indent=2)
