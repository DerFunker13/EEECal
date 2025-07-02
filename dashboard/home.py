import tkinter as tk

def create_frame(parent):
    frame = tk.Frame(parent, bg="white")
    label = tk.Label(frame, text="Welcome to the Home Module!", font=("Arial", 16), bg="white")
    label.pack(padx=20, pady=20)
    return frame
