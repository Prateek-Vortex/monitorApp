from threading import Event

# Shared state object
paused = Event()
paused.clear()

# Trackable stats
stats = {
    "active_seconds": 0,
    "idle_count": 0,
    "reminder_count": 0,
    "app_usage": {}  # new!
}
