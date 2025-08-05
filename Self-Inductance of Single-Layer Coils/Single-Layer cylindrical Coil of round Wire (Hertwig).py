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
KDl=[
    [0.00,  0.02,  0.04,  0.06,  0.08,  0.10,  0.12, 0.14, 0.16, 0.18, 0.20, 0.22, 0.24, 0.26, 0.28, 0.30, 0.32, 0.34, 0.36, 0.38, 0.40, 0.42, 0.44, 0.46, 0.48, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00, 1.10, 1.20, 1.30, 1.40, 1.50, 1.60, 1.70, 1.80, 1.90, 2.00, 2.20, 2.40, 2.60, 2.80, 3.00, 3.50, 4.00, 4.50, 5.00, 6.00, 7.00, 8.00, 9.00, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0],
    [0.0000,0.1957,0.3882,0.5776,0.7643,0.9465,1.126,1.303,1.477,1.648,1.817,1.982,2.144,2.305,2.446,2.616,2.769,2.919,3.067,3.212,3.355,3.497,3.635,3.771,3.905,4.039,4.358,4.668,4.969,5.256,5.535,5.803,6.063,6.271,6.559,6.795,7.244,7.610,8.060,8.453,8.811,9.154,9.480,9.769,10.09,10.37,10.93,11.41,12.01,12.30,12.71,13.63,14.43,15.14,15.78,16.90,17.85,18.68,19.41,20.07,21.21,22.18,23.01,23.76,24.40,25.78,26.93,27.87,28.74,29.53,30.16,31.26,32.24,33.11,33.86,34.53],
#Korrektur! Originale: 0.28:2.406; 0.90:6.171; 1.20:7.510; 1.80:9.569; 2.60:12.01
]

# Unit conversion factors
unit_factors_length = {"m": 1.0, "cm": 0.01, "mm": 0.001}
unit_factors_inductance = {"H": 1.0, "mH": 1e3, "µH": 1e6, "nH": 1e9}
unit_factors_frequency = {"Hz": 1.0, "kHz": 1e3, "MHz": 1e6, "GHz": 1e9}

def create_frame(parent):
    frame = tk.Frame(parent, bg="white")

    # --- Title -----------------------------
    title_label = tk.Label(frame, text="Self-Inductance of Single-Layer cylindrical Coil of round Wire (low. freq.)", font=("Arial", 16, "bold"), bg="white")
    title_label.grid(row=0, column=0, columnspan=6, sticky="w", padx=10, pady=10)

    # --- Image (Top-Right) ----------------
    image_path = os.path.join(os.path.dirname(__file__), "pic_cylinder coil round wire.jpg")
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
    labels = ["Coil Diameter D", "Coil Length l", "Number of turns w"]
    entries = []
    default_values = ["2","20","100"]

    diameter_unit_var = tk.StringVar(value="cm")
    length_unit_var = tk.StringVar(value="cm")
    output_unit_var = tk.StringVar(value="µH")

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
                         textvariable=length_unit_var).grid(row=i + 2, column=2, padx=(2, 0))
    # --- Result Output ---------------------
    result_label = tk.Label(frame, text="Inductance L₀", bg="white", anchor="w")
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
            l = float(entries[1].get())*100* unit_factors_length[length_unit_var.get()] #m->cm
            w=float(entries[2].get())
            
            (flag, K)=interpolate(KDl[0], KDl[1], (D/l))

            if flag==1:
                result_var.set("Invalid input!")
            
            inductance =  (K*w**2*D)*10**(-9)* unit_factors_inductance[output_unit_var.get()]
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
        text=r"Harry Hertwig: Induktivitäten. Berlin: Verlag für Radio-Foto-Kinotechnik. 1954. Induktivität einlagiger Zylinderspulen aus Runddraht.",
        bg="white",
        font=("Arial", 10),
        fg="gray"
    )
    footer.grid(row=15, column=0, columnspan=8, pady=(10, 10))

    return frame