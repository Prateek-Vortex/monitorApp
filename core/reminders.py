from api.state import stats
from core.gpt import get_gpt_reminder
from core.logger import log_action
from system.tray import show_reminder_popup

def maybe_trigger_reminder(active_time_counter, threshold):
    if active_time_counter >= threshold:
        reminder = get_gpt_reminder()
        show_reminder_popup(reminder)
        log_action("Reminder shown", reminder)
        stats["reminder_count"] += 1
        return 0
    return active_time_counter


def maybe_trigger_reminder_test(active_time_counter, threshold):
    print("✅ Simulating a test reminder...")
    reminder = get_gpt_reminder()
    show_reminder_popup(reminder)
    log_action("Reminder shown", reminder)
    stats["reminder_count"] += 1
    return 0

