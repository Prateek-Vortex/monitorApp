from fastapi import FastAPI
from api.state import paused, stats
from core.reminders import show_test_reminder
import uvicorn
import threading
from core.tracker import start_tracking

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


if __name__ == "__main__":
    uvicorn.run("api.server:app", host="0.0.0.0", port=5001, reload=False)
