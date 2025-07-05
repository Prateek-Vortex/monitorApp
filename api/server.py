from fastapi import FastAPI
from api.state import paused, stats
from core.reminders import show_test_reminder
import uvicorn
import threading
from core.tracker import start_tracking
from fastapi import Query
from datetime import datetime, timedelta
import json

app = FastAPI()

@app.post("/pause")
def pause_tracking():
    paused.set()
    return {"status": "paused"}

@app.post("/resume")
def resume_tracking():
    paused.clear()
    return {"status": "resumed"}

@app.get("/stats")
def get_stats():
    return {
        "active_minutes": round(stats["active_seconds"] / 60, 1),
        "idle_events": stats["idle_count"],
        "reminders_sent": stats["reminder_count"]
    }

@app.get("/test-reminder")
def test_reminder():
    show_test_reminder()
    return {"status": "Reminder triggered manually"}

@app.on_event("startup")
def begin_tracking():
    print("✅ FocusBae tracker started...")
    threading.Thread(target=start_tracking, daemon=True).start()

@app.get("/app-usage")
def get_app_usage(since_minutes: int = Query(default=1440)):  # default = last 24h
    now = datetime.now()
    cutoff = now - timedelta(minutes=since_minutes)

    # Load screen log from disk
    with open("data/focusbae_screenlog.json", "r") as f:
        log = json.load(f)

    usage = {}
    for entry in log:
        ts = datetime.fromisoformat(entry["timestamp"])
        if ts < cutoff or entry["activity"] != "Active screen":
            continue
        app = entry["detail"]
        usage[app] = usage.get(app, 0) + 60  # assuming LOG_INTERVAL = 60

    # Return usage in minutes
    sorted_usage = sorted(usage.items(), key=lambda x: x[1], reverse=True)
    return {app: round(secs / 60, 1) for app, secs in sorted_usage}


if __name__ == "__main__":
    uvicorn.run("api.server:app", host="0.0.0.0", port=5001, reload=False)
