import tkinter as tk
from tkinter import messagebox
import time
import threading
import csv
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

CSV_FILE = "pomodoro_sessions.csv"

# Log task session to CSV
def log_session(task):
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), task])

# Timer logic
def start_timer(duration, label, task_entry, phase):
    task = task_entry.get().strip()
    if phase == "work" and not task:
        messagebox.showwarning("Missing Task", "Please enter a task name.")
        return

    def countdown():
        seconds = duration * 60
        while seconds:
            mins, secs = divmod(seconds, 60)
            label.config(text=f"{phase.capitalize()} Time: {mins:02}:{secs:02}")
            time.sleep(1)
            seconds -= 1
        label.config(text=f"{phase.capitalize()} complete!")

        if phase == "work":
            log_session(task)
            messagebox.showinfo("Done", f"Pomodoro completed for task: {task}")
            start_timer(5, label, task_entry, "break")
        else:
            messagebox.showinfo("Break Over", "Time to start a new Pomodoro!")

    thread = threading.Thread(target=countdown)
    thread.start()

# Chart display
def show_summary_chart():
    try:
        df = pd.read_csv(CSV_FILE, names=["timestamp", "task"])
        df['minutes'] = 25
        summary = df.groupby('task')['minutes'].sum().sort_values(ascending=False)

        if summary.empty:
            messagebox.showinfo("No Data", "No Pomodoro sessions logged yet.")
            return

        plt.figure(figsize=(8, 5))
        summary.plot(kind='bar', color='tomato')
        plt.title("Total Time Spent per Task")
        plt.xlabel("Task")
        plt.ylabel("Minutes")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
    except FileNotFoundError:
        messagebox.showwarning("No Data File", "No session data found.")

# GUI
def create_gui():
    root = tk.Tk()
    root.title("Pomodoro Timer with Task Tracker")
    root.geometry("350x250")
    root.resizable(False, False)

    tk.Label(root, text="Enter Task Name:", font=("Helvetica", 12)).pack(pady=5)
    task_entry = tk.Entry(root, width=35)
    task_entry.pack(pady=5)

    label = tk.Label(root, text="Ready to focus?", font=("Helvetica", 12))
    label.pack(pady=10)

    tk.Button(root, text="Start Pomodoro", command=lambda: start_timer(25, label, task_entry, "work")).pack(pady=5)
    tk.Button(root, text="Show Time Spent Chart", command=show_summary_chart).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
