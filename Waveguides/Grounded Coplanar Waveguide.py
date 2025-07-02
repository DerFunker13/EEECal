import tkinter as tk
from tkinter import messagebox

def create_frame(parent):
    frame = tk.Frame(parent, bg="white")

    label = tk.Label(frame, text="Additor Module", font=("Arial", 16), bg="white")
    label.pack(pady=(20, 10))

    entry1 = tk.Entry(frame, font=("Arial", 14))
    entry1.pack(pady=5)

    entry2 = tk.Entry(frame, font=("Arial", 14))
    entry2.pack(pady=5)

    result_label = tk.Label(frame, text="", font=("Arial", 14), bg="white")
    result_label.pack(pady=10)

    def add_numbers():
        try:
            num1 = float(entry1.get())
            num2 = float(entry2.get())
            result = num1 + num2
            result_label.config(text=f"Result: {result}")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers.")

    add_button = tk.Button(frame, text="Add", command=add_numbers, font=("Arial", 12))
    add_button.pack(pady=10)

    return frame