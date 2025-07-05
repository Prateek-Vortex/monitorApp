from fastapi import FastAPI
from api.state import paused, stats
import uvicorn

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

if __name__ == "__main__":
    uvicorn.run("api.server:app", host="0.0.0.0", port=5001, reload=False)
