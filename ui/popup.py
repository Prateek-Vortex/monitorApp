import tkinter as tk
from tkinter import messagebox
import subprocess

# def show_reminder_popup(message):
#     popup = tk.Tk()
#     popup.withdraw()
#     messagebox.showinfo("FocusBae 💧", message)
#     popup.destroy()



import subprocess
import shlex

def show_reminder_popup(message: str):
    try:
        # Escape double quotes in the message
        safe_message = message.replace('"', '\\"')

        script = f'display notification "{safe_message}" with title "FocusBae 💧"'
        command = ["osascript", "-e", script]

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.stderr:
            print("❌ AppleScript error:", result.stderr)
        else:
            print("✅ Notification sent!")

    except Exception as e:
        print("❌ Exception sending notification:", e)

