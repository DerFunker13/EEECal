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

# --- Unit conversion factors ----------------
unit_factors_length = {"m": 1.0, "cm": 0.01, "mm": 0.001}
unit_factors_inductance = {"H": 1.0, "mH": 1e3, "µH": 1e6, "nH": 1e9}

def create_frame(parent):
    frame = tk.Frame(parent, bg="white")

    # --- Title -----------------------------
    title_label = tk.Label(frame, text="Self-Inductance of a Cage (low freq.)", font=("Arial", 16, "bold"), bg="white")
    title_label.grid(row=0, column=0, columnspan=4, sticky="w", padx=10, pady=10)

    # --- Image (Top-Right) ----------------
    image_path = os.path.join(os.path.dirname(__file__), "pic_cage.jpg")
    try:
        image = Image.open(image_path)
        image = image.resize((250, 200))
        photo = ImageTk.PhotoImage(image)
        image_label = tk.Label(frame, image=photo, bg="white")
        image_label.image = photo
        image_label.grid(row=1, column=4, rowspan=10, sticky="ne", padx=10, pady=10)
    except Exception as e:
        print("Image load error:", e)

    # --- Entry Fields with Unit Selection ---------------------
    labels = ["Length l", "Radius ρ", "Diameter d", "Line number n"]
    entries = []
    default_values = ["3", "12.5", "0.5", "6"]

    # Unit selectors
    length_unit_var = tk.StringVar(value="m")
    radius_unit_var = tk.StringVar(value="cm")
    diameter_unit_var = tk.StringVar(value="cm")

    for i, text in enumerate(labels):
        lbl = tk.Label(frame, text=text, bg="white", anchor="w")
        lbl.grid(row=i + 2, column=0, sticky="w", padx=10, pady=5)

        ent = tk.Entry(frame, width=20, textvariable=tk.StringVar(value=default_values[i]))
        ent.grid(row=i + 2, column=1, padx=0, pady=5)
        entries.append(ent)

        # Unit selectors
        if i == 0:  # Length
            unit_cb = ttk.Combobox(frame, values=list(unit_factors_length.keys()), width=5, state="readonly",
                                   textvariable=length_unit_var)
            unit_cb.grid(row=i + 2, column=2, padx=5)
        elif i == 1:  # Radius
            unit_cb = ttk.Combobox(frame, values=list(unit_factors_length.keys()), width=5, state="readonly",
                                   textvariable=radius_unit_var)
            unit_cb.grid(row=i + 2, column=2, padx=5)
        elif i == 2:  # Diameter
            unit_cb = ttk.Combobox(frame, values=list(unit_factors_length.keys()), width=5, state="readonly",
                                   textvariable=diameter_unit_var)
            unit_cb.grid(row=i + 2, column=2, padx=5)

    # --- Result Output ---------------------
    result_label = tk.Label(frame, text="Inductance L", bg="white", anchor="w")
    result_label.grid(row=7, column=0, sticky="w", padx=10, pady=(15, 5))

    result_var = tk.StringVar()
    result_entry = tk.Entry(frame, textvariable=result_var, width=20, state="readonly")
    result_entry.grid(row=7, column=1, padx=10, pady=(15, 5))

    # Output unit selector
    output_unit_var = tk.StringVar(value="µH")
    output_unit_cb = ttk.Combobox(frame, values=list(unit_factors_inductance.keys()), width=5,
                                  textvariable=output_unit_var, state="readonly")
    output_unit_cb.grid(row=7, column=2, padx=(2, 0), pady=(15, 5))

    precision_label = tk.Label(frame, text="Error < 5%", bg="white", anchor="w")
    precision_label.grid(row=7, column=3, sticky="w", padx=10, pady=5)

    # --- Calculate Button ------------------
    def calculate():
        try:
            l = float(entries[0].get())*100 #m->cm
            rho = float(entries[1].get())*100 #m->cm
            d = float(entries[2].get())*100 #m->cm
            n = int(entries[3].get())

            # Convert to meters
            l = l * unit_factors_length[length_unit_var.get()]
            rho = rho * unit_factors_length[radius_unit_var.get()]
            d = d * unit_factors_length[diameter_unit_var.get()]

            # Interpolated value based on Hertwig's method or similar
            L_H = (2*l*(np.log(2*l/np.power((0.3894*d*n*np.power(rho,n-1)),1/n))-1)) * 10**(-9)

            # Convert output
            output_unit = output_unit_var.get()
            converted_L = L_H * unit_factors_inductance[output_unit]

            result_var.set(f"{converted_L:.4e}")
        except Exception as e:
            result_var.set("Invalid input!")

    calc_button = tk.Button(frame, text="Calculate", command=calculate, bg="#e1e1e1")
    calc_button.grid(row=8, column=1, columnspan=1, pady=(10, 5))

    # --- Footer ----------------------------
    footer = tk.Label(
        frame,
        text=r"Harry Hertwig: Induktivitäten. Berlin: Verlag für Radio-Foto-Kinotechnik. 1954. Selbstinduktivität einer Reuse.",
        bg="white",
        font=("Arial", 10),
        fg="gray"
    )
    footer.grid(row=12, column=0, columnspan=6, pady=(10, 10))

    return frame
