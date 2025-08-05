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

# Unit conversion factors
unit_factors_length = {"m": 1.0, "cm": 0.01, "mm": 0.001}
unit_factors_inductance = {"H": 1.0, "mH": 1e3, "µH": 1e6, "nH": 1e9}
unit_factors_frequency = {"Hz": 1.0, "kHz": 1e3, "MHz": 1e6, "GHz": 1e9}

def create_frame(parent):
    frame = tk.Frame(parent, bg="white")

    # --- Title -----------------------------
    title_label = tk.Label(frame, text="Self-Inductance of a flat band ring (low. freq.)", font=("Arial", 16, "bold"), bg="white")
    title_label.grid(row=0, column=0, columnspan=3, sticky="w", padx=10, pady=10)

    # --- Image (Top-Right) ----------------
    image_path = os.path.join(os.path.dirname(__file__), "pic_flat band ring.jpg")
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
    labels = ["Diameter D", "Width b"]
    entries = []
    default_values = ["50","50"]

    diameter_unit_var = tk.StringVar(value="cm")
    width_unit_var = tk.StringVar(value="mm")
    output_unit_var = tk.StringVar(value="H")

    for i, text in enumerate(labels):
        lbl = tk.Label(frame, text=text, bg="white", anchor="w")
        lbl.grid(row=i+2, column=0, sticky="w", padx=10, pady=5)

        ent = tk.Entry(frame, width=20, textvariable=tk.StringVar(value=default_values[i]))
        ent.grid(row=i+2, column=1, padx=10, pady=5)
        entries.append(ent)
        
        if i == 0:
            ttk.Combobox(frame, values=list(unit_factors_length.keys()), width=5, state="readonly",
                         textvariable=diameter_unit_var).grid(row=i + 2, column=2, padx=(2, 0))
        elif i == 1:
            ttk.Combobox(frame, values=list(unit_factors_length.keys()), width=5, state="readonly",
                         textvariable=width_unit_var).grid(row=i + 2, column=2, padx=(2, 0))
    # --- Text ------------------------------

    hinweise = tk.Label(frame, text="Thickness << Width", bg="white", anchor="w")
    hinweise.grid(row=4, column=1, padx=10, pady=5)
    # --- Result Output ---------------------
    result_label = tk.Label(frame, text="Inductance (H)", bg="white", anchor="w")
    result_label.grid(row=12, column=0, sticky="w", padx=10, pady=(15, 5))

    result_var = tk.StringVar()
    result_entry = tk.Entry(frame, textvariable=result_var, width=20, state="readonly")
    result_entry.grid(row=12, column=1, padx=10, pady=(15, 5))

    precision_label = tk.Label(frame, text="Error < 5%", bg="white", anchor="w")
    precision_label.grid(row=12, column=3, sticky="w", padx=10, pady=5)

    ttk.Combobox(frame, values=list(unit_factors_inductance.keys()), width=5,
                 textvariable=output_unit_var, state="readonly").grid(row=12, column=2, padx=(2, 0), pady=(15, 5))
    # --- Calculate Button ------------------
    def calculate():
        try:
            D = float(entries[0].get())*100* unit_factors_length[diameter_unit_var.get()] #m->cm
            b = float(entries[1].get())*100* unit_factors_length[width_unit_var.get()] #m->cm
            
            inductance =  (2*np.pi*D*(np.log(4*D/b)-0.5))*10**(-9)* unit_factors_inductance[output_unit_var.get()]
            result_var.set(f"{inductance:.4e}")
        except ValueError:
            result_var.set("Invalid input!")

    calc_button = tk.Button(frame, text="Calculate", command=calculate, bg="#e1e1e1")
    calc_button.grid(row=13, column=1, columnspan=1, pady=(10, 5))

    
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
        text=r"Harry Hertwig: Induktivitäten. Berlin: Verlag für Radio-Foto-Kinotechnik. 1954. Induktivität eines Ringes aus Flachband.",
        bg="white",
        font=("Arial", 10),
        fg="gray"
    )
    footer.grid(row=15, column=0, columnspan=8, pady=(10, 10))

    return frame