from pystray import Icon, MenuItem as Item
from PIL import Image, ImageDraw
import threading
import sys

paused = threading.Event()
paused.clear()

def create_image():
    img = Image.new("RGB", (64, 64), "white")
    draw = ImageDraw.Draw(img)
    draw.ellipse((16, 16, 48, 48), fill="blue")
    return img

def toggle_pause(icon, item):
    if paused.is_set():
        paused.clear()
        print("🔔 Reminders resumed")
    else:
        paused.set()
        print("🔕 Reminders paused")

def show_about(icon, item):
    print("FocusBae — Your AI-powered wellness companion!")

def on_exit(icon, item):
    print("Exiting FocusBae...")
    icon.stop()
    sys.exit()

def setup_tray():
    icon = Icon(
        "focusbae",
        create_image(),
        "FocusBae",
        menu=(
            Item("About", show_about),
            Item("Pause/Resume Reminders", toggle_pause),
            Item("Exit", on_exit)
        )
    )
    threading.Thread(target=icon.run, daemon=True).start()
