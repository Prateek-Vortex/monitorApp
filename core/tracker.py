import time
import threading
import subprocess
import os
from pynput import mouse, keyboard
from api.state import paused, stats


from config import IDLE_THRESHOLD, LOG_INTERVAL, REMINDER_THRESHOLD
from core.logger import log_action
from core.reminders import maybe_trigger_reminder

last_active_time = time.time()
is_idle = False
active_time_counter = 0

def on_input(_):
    global last_active_time, is_idle
    last_active_time = time.time()
    if is_idle:
        log_action("Back to active")
        is_idle = False

def track_input_activity():
    with mouse.Listener(on_move=on_input, on_click=on_input, on_scroll=on_input) as ml, \
         keyboard.Listener(on_press=on_input) as kl:
        ml.join()
        kl.join()

def get_foreground_app():
    try:
        if os.name == "posix":
            result = subprocess.run(
                ["osascript", "-e", 'tell application "System Events" to get name of (processes where frontmost is true)'],
                stdout=subprocess.PIPE,
                text=True
            )
            return result.stdout.strip().split(",")[0]
        elif os.name == "nt":
            import win32gui
            window = win32gui.GetForegroundWindow()
            return win32gui.GetWindowText(window)
        else:
            return "UnknownOS"
    except Exception as e:
        return f"Error: {e}"


def start_tracking():
    global is_idle, active_time_counter, last_active_time
    while True:
        if paused.is_set():
            print("⏸️ Paused... skipping reminder logic")
            time.sleep(5)
            continue

        now = time.time()
        if now - last_active_time > IDLE_THRESHOLD:
            if not is_idle:
                log_action("Idle started")
                stats["idle_count"] += 1
                is_idle = True
        else:
            app = get_foreground_app()
            log_action("Active screen", app)
            stats["active_seconds"] += LOG_INTERVAL
            active_time_counter += LOG_INTERVAL
            active_time_counter = maybe_trigger_reminder(active_time_counter, REMINDER_THRESHOLD)

        time.sleep(LOG_INTERVAL)
# def start_tracking():
#     global is_idle, active_time_counter
#     threading.Thread(target=track_input_activity, daemon=True).start()

#     while True:
#         now = time.time()
#         if paused.is_set():
#             time.sleep(5)
#             continue

#         # When active
#         stats["active_seconds"] += LOG_INTERVAL
#         if now - last_active_time > IDLE_THRESHOLD:
#             if not is_idle:
#                 log_action("Idle started")
#                 stats["idle_count"] += 1  
#                 is_idle = True
#         else:
#             app = get_foreground_app()
#             log_action("Active screen", app)
#             active_time_counter += LOG_INTERVAL
#             active_time_counter = maybe_trigger_reminder(active_time_counter, REMINDER_THRESHOLD)

#         time.sleep(LOG_INTERVAL)
