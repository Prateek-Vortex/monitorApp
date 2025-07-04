import tkinter as tk
from tkinter import messagebox

def show_reminder_popup(message):
    popup = tk.Tk()
    popup.withdraw()
    messagebox.showinfo("FocusBae 💧", message)
    popup.destroy()
