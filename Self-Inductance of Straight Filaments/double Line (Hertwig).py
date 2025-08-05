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

# Unit conversion factors
unit_factors_length = {"m": 1.0, "cm": 0.01, "mm": 0.001}
unit_factors_inductance = {"H": 1.0, "mH": 1e3, "µH": 1e6, "nH": 1e9}
unit_factors_frequency = {"Hz": 1.0, "kHz": 1e3, "MHz": 1e6, "GHz": 1e9}


def create_frame(parent):
    frame = tk.Frame(parent, bg="white")

    # --- Title -----------------------------
    title_label = tk.Label(frame, text="Self-Inductance of a double line (forward and return)", font=("Arial", 16, "bold"), bg="white")
    title_label.grid(row=0, column=0, columnspan=4, sticky="w", padx=10, pady=10)

    # --- Image (Top-Right) ----------------
    image_path = os.path.join(os.path.dirname(__file__), "pic_round twin line.jpg")
    try:
        image = Image.open(image_path)
        image = image.resize((200, 125))
        photo = ImageTk.PhotoImage(image)
        image_label = tk.Label(frame, image=photo, bg="white")
        image_label.image = photo
        image_label.grid(row=1, column=4, rowspan=10, sticky="ne", padx=10, pady=10)
    except Exception as e:
        print("Image load error:", e)

    # --- Entry Fields ---------------------
    labels = ["Length l", "Diameter d", "Distance a", "rel. Permeability μᵣ", "Frequency f", "Conductance ϰ"]
    entries = []
    default_values = ["3", "5", "25", "1", "0", "59600000.0"]

    # Unit variables
    length_unit_var = tk.StringVar(value="m")
    diameter_unit_var = tk.StringVar(value="mm")
    distance_unit_var = tk.StringVar(value="cm")
    frequency_unit_var = tk.StringVar(value="Hz")

    for i, text in enumerate(labels):
        lbl = tk.Label(frame, text=text, bg="white", anchor="w")
        lbl.grid(row=i+2, column=0, sticky="w", padx=10, pady=5)

        ent = tk.Entry(frame, width=20, textvariable=tk.StringVar(value=default_values[i]))
        ent.grid(row=i+2, column=1, padx=0, pady=5)
        entries.append(ent)

        if i == 0:
            cb = ttk.Combobox(frame, values=list(unit_factors_length.keys()), width=5, textvariable=length_unit_var, state="readonly")
            cb.grid(row=i+2, column=2)
        elif i == 1:
            cb = ttk.Combobox(frame, values=list(unit_factors_length.keys()), width=5, textvariable=diameter_unit_var, state="readonly")
            cb.grid(row=i+2, column=2)
        elif i == 2:
            cb = ttk.Combobox(frame, values=list(unit_factors_length.keys()), width=5, textvariable=distance_unit_var, state="readonly")
            cb.grid(row=i+2, column=2)
        elif i == 4:
            cb = ttk.Combobox(frame, values=list(unit_factors_frequency.keys()), width=5, textvariable=frequency_unit_var, state="readonly")
            cb.grid(row=i+2, column=2)
        elif i == 5:
            cond_unit = tk.Label(frame, text="S/m", bg="white", anchor="w")
            cond_unit.grid(row=i + 2, column=2, padx=10, pady=5)

    # --- Permeability ComboBox -------------
    def on_mu_select(event):
        selected = mu_cb.get()
        match = next((v for v, mat in mu_table if mat == selected), None)
        if match is not None:
            entries[3].delete(0, tk.END)
            entries[3].insert(0, str(match))

    mu_cb_label = tk.Label(frame, text="Material (μᵣ)", bg="white", anchor="w")
    mu_cb_label.grid(row=4, column=3, sticky="w", padx=10, pady=(5, 0))

    mu_cb = ttk.Combobox(frame, values=[mat for _, mat in mu_table], width=20)
    mu_cb.grid(row=5, column=3, padx=10, pady=(5, 0))
    mu_cb.bind("<<ComboboxSelected>>", on_mu_select)

    # --- Conductance ComboBox --------------
    def on_cond_select(event):
        selected = cond_cb.get()
        match = next((v for v, mat in conductance_table if mat == selected), None)
        if match is not None:
            entries[5].delete(0, tk.END)
            entries[5].insert(0, str(match))

    cond_cb_label = tk.Label(frame, text="Material (ϰ)", bg="white", anchor="w")
    cond_cb_label.grid(row=6, column=3, sticky="w", padx=10, pady=(5, 0))

    cond_cb = ttk.Combobox(frame, values=[mat for _, mat in conductance_table], width=20)
    cond_cb.current(0)
    cond_cb.grid(row=7, column=3, padx=10, pady=(5, 0))
    cond_cb.bind("<<ComboboxSelected>>", on_cond_select)

    # --- Result Output ---------------------
    result_label = tk.Label(frame, text="Inductance L", bg="white", anchor="w")
    result_label.grid(row=9, column=0, sticky="w", padx=10, pady=(15, 5))

    result_var = tk.StringVar()
    result_entry = tk.Entry(frame, textvariable=result_var, width=20, state="readonly")
    result_entry.grid(row=9, column=1, padx=10, pady=(15, 5))

    # Output unit selection
    output_unit_var = tk.StringVar(value="µH")
    output_unit_cb = ttk.Combobox(frame, values=list(unit_factors_inductance.keys()), width=5,
                                  textvariable=output_unit_var, state="readonly")
    output_unit_cb.grid(row=9, column=2, padx=(2, 0), pady=(15, 5))

    precision_label = tk.Label(frame, text="Error < 5%", bg="white", anchor="w")
    precision_label.grid(row=9, column=3, sticky="w", padx=10, pady=5)

    # --- Calculate Button ------------------
    def calculate():
        try:
            l = float(entries[0].get())
            d = float(entries[1].get())
            a = float(entries[2].get())
            mu_r = float(entries[3].get())
            f = float(entries[4].get())
            kappa = float(entries[5].get())

            # Convert units
            l_m = l * unit_factors_length[length_unit_var.get()]
            d_m = d * unit_factors_length[diameter_unit_var.get()]
            a_m = a * unit_factors_length[distance_unit_var.get()]
            f_Hz = f * unit_factors_frequency[frequency_unit_var.get()]

            delta = hertwig_skineffekt(f_Hz, kappa, d_m)

            # Calculate inductance in Henry
            L_H = 4 * l_m * 100 * (np.log(2* a_m / d_m) -(a_m / l_m)+ (mu_r * delta )) * 1e-9

            # Convert to output unit
            output_unit = output_unit_var.get()
            converted_L = L_H * unit_factors_inductance[output_unit]
            result_var.set(f"{converted_L:.4e}")
        except ValueError:
            result_var.set("Invalid input!")

    calc_button = tk.Button(frame, text="Calculate", command=calculate, bg="#e1e1e1")
    calc_button.grid(row=10, column=1, columnspan=1, pady=(10, 5))

    # --- Footer ----------------------------
    footer = tk.Label(
        frame,
        text=r"Harry Hertwig: Induktivitäten. Berlin: Verlag für Radio-Foto-Kinotechnik. 1954. Selbstinduktivität einer Doppelleitung",
        bg="white",
        font=("Arial", 10),
        fg="gray"
    )
    footer.grid(row=12, column=0, columnspan=6, pady=(10, 10))

    return frame
