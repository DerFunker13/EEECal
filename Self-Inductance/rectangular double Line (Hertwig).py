import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import sys
import os
import numpy as np

# Add the parent directory (EEECal) to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import lookup tables
from addresources.epsilon import epsilon_table
from addresources.conductance import conductance_table
from addresources.mu import mu_table
from addresources.skineffektfaktor import hertwig_skineffekt
from addresources.interpolate import interpolate

#local tables:


def create_frame(parent):
    frame = tk.Frame(parent, bg="white")

    # --- Title -----------------------------
    title_label = tk.Label(frame, text="Self-Inductance of a rectangular double line(low freq.)", font=("Arial", 16, "bold"), bg="white")
    title_label.grid(row=0, column=0, columnspan=3, sticky="w", padx=10, pady=10)

    # --- Image (Top-Right) ----------------
    image_path = os.path.join(os.path.dirname(__file__), "pic_rectangular double line.png")
    try:
        image = Image.open(image_path)
        image = image.resize((250, 200))
        photo = ImageTk.PhotoImage(image)
        image_label = tk.Label(frame, image=photo, bg="white")
        image_label.image = photo
        image_label.grid(row=1, column=3, rowspan=10, sticky="ne", padx=10, pady=10)
    except Exception as e:
        print("Image load error:", e)

    # --- Entry Fields ---------------------
    labels = ["Length l (m)", "Space between centers a (m)", "Width b (m)", "Thickness c (m)"]
    entries = []
    default_values = ["3","25e-2","8e-3","2.5e-3"]

    for i, text in enumerate(labels):
        lbl = tk.Label(frame, text=text, bg="white", anchor="w")
        lbl.grid(row=i+2, column=0, sticky="w", padx=10, pady=5)

        ent = tk.Entry(frame, width=30, textvariable=tk.StringVar(value=default_values[i]))
        ent.grid(row=i+2, column=1, padx=10, pady=5)
        entries.append(ent)

    # --- Result Output ---------------------
    result_label = tk.Label(frame, text="Inductance (H)", bg="white", anchor="w")
    result_label.grid(row=12, column=0, sticky="w", padx=10, pady=(15, 5))

    result_var = tk.StringVar()
    result_entry = tk.Entry(frame, textvariable=result_var, width=30, state="readonly")
    result_entry.grid(row=12, column=1, padx=10, pady=(15, 5))

    precision_label = tk.Label(frame, text="Error < 5%", bg="white", anchor="w")
    precision_label.grid(row=12, column=2, sticky="w", padx=10, pady=5)
    # --- Calculate Button ------------------
    def calculate():
        try:
            l = float(entries[0].get())*100 #m->cm
            a = float(entries[1].get())*100 #m->cm
            b = float(entries[2].get())*100 #m->cm
            c = float(entries[3].get())*100 #m->cm

            inductance =  (4*l*(np.log(a/(b+c)) + 1.5 - a/l + 0.2235*(b+c)/l)) * 10**(-9)
            result_var.set(f"{inductance:.4e}")
        except ValueError:
            result_var.set("Invalid input!")

    calc_button = tk.Button(frame, text="Calculate", command=calculate, bg="#e1e1e1")
    calc_button.grid(row=13, column=0, columnspan=2, pady=(10, 5))

    
    # --- Text ----------------------------
#    text = tk.Text(
#        frame,
#        bg="white",
#        font=("Arial", 12),
#        fg="gray"
#    )
#    text.grid(row=14, column=0, columnspan=4, pady=(10, 10))
#    
#    quote = """ """
#    text.insert("1.0",quote)
    
    # --- Footer ----------------------------
    footer = tk.Label(
        frame,
        text=r"Harry Hertwig: Induktivitäten. Berlin: Verlag für Radio-Foto-Kinotechnik. 1954. Induktivität einer Doppelleitung mit rechteckigen Leiterquerschnitt.",
        bg="white",
        font=("Arial", 10),
        fg="gray"
    )
    footer.grid(row=15, column=0, columnspan=3, pady=(10, 10))

    return frame