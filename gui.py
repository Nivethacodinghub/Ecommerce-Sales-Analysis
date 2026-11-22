import tkinter as tk
from tkinter import messagebox
import os
import subprocess
import sys

folder = os.path.dirname(os.path.abspath(__file__))

root = tk.Tk()
root.title("E-Commerce Sales Analysis")
root.geometry("700x500")
root.configure(bg="#EAF2F8")
root.resizable(False, False)

# Heading
title = tk.Label(
    root,
    text="E-COMMERCE SALES ANALYSIS",
    font=("Arial", 23, "bold"),
    bg="#EAF2F8",
    fg="#154360"
)
title.pack(pady=35)

subtitle = tk.Label(
    root,
    text="Sales Data Analysis Using Python",
    font=("Arial", 14),
    bg="#EAF2F8",
    fg="#2874A6"
)
subtitle.pack(pady=5)


# Open Dashboard
def open_dashboard():
    path = os.path.join(folder, "dashboard.png")

    if os.path.exists(path):
        os.startfile(path)
    else:
        messagebox.showerror("Error", "Dashboard not found!")


# Run Analysis
def run_analysis():
    path = os.path.join(folder, "analysis.py")

    if os.path.exists(path):
        subprocess.Popen([sys.executable, path])
    else:
        messagebox.showerror("Error", "Analysis file not found!")


# Exit
def exit_program():
    root.destroy()


# Button style
style = {
    "font": ("Arial", 13, "bold"),
    "width": 25,
    "height": 2,
    "bg": "#2874A6",
    "fg": "white",
    "cursor": "hand2"
}

tk.Button(
    root,
    text="Run Sales Analysis",
    command=run_analysis,
    **style
).pack(pady=20)

tk.Button(
    root,
    text="View Sales Dashboard",
    command=open_dashboard,
    **style
).pack(pady=15)

tk.Button(
    root,
    text="Exit",
    command=exit_program,
    **style
).pack(pady=15)


footer = tk.Label(
    root,
    text="Developed Using Python | Pandas | Matplotlib | Tkinter",
    font=("Arial", 10),
    bg="#EAF2F8",
    fg="#566573"
)
footer.pack(side="bottom", pady=20)

root.mainloop()
