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
    title_label = tk.Label(frame, text="Self-Inductance of a square Wire Loop", font=("Arial", 16, "bold"), bg="white")
    title_label.grid(row=0, column=0, columnspan=3, sticky="w", padx=10, pady=10)

    # --- Image (Top-Right) ----------------
    image_path = os.path.join(os.path.dirname(__file__), "pic_square wire loop.jpg")
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
    labels = ["Side length s", "Wire diameter d", "rel. Permeability μᵣ", "Frequency f", "Conductance ϰ"]
    entries = []
    default_values = ["50","10","1","10","59600000.0"]

    sidelength_unit_var = tk.StringVar(value="cm")
    diameter_unit_var = tk.StringVar(value="mm")
    frequency_unit_var = tk.StringVar(value="MHz")
    output_unit_var = tk.StringVar(value="H")

    for i, text in enumerate(labels):
        lbl = tk.Label(frame, text=text, bg="white", anchor="w")
        lbl.grid(row=i+2, column=0, sticky="w", padx=10, pady=5)

        ent = tk.Entry(frame, width=20, textvariable=tk.StringVar(value=default_values[i]))
        ent.grid(row=i+2, column=1, padx=10, pady=5)
        entries.append(ent)

        # Add unit selection for length and diameter
        if i == 0:
            length_unit_cb = ttk.Combobox(frame, values=list(unit_factors_length.keys()), width=5, state="readonly",
                                          textvariable=sidelength_unit_var)
            length_unit_cb.grid(row=i + 2, column=2, padx=(2, 0))
        elif i == 1:
            diameter_unit_cb = ttk.Combobox(frame, values=list(unit_factors_length.keys()), width=5, state="readonly",
                                            textvariable=diameter_unit_var)
            diameter_unit_cb.grid(row=i + 2, column=2, padx=(2, 0))
        elif i == 3:
            frequency_unit_cb = ttk.Combobox(frame, values=list(unit_factors_frequency.keys()), width=5, state="readonly",
                                            textvariable=frequency_unit_var)
            frequency_unit_cb.grid(row=i + 2, column=2, padx=(2, 0))
        elif i == 4:
            cond_unit = tk.Label(frame, text="S/m", bg="white", anchor="w")
            cond_unit.grid(row=i + 2, column=2, padx=10, pady=5)

    # --- Permeability ComboBox -------------
    def on_mu_select(event):
        selected = mu_cb.get()
        match = next((v for v, mat in mu_table if mat == selected), None)
        if match is not None:
            entries[2].delete(0, tk.END)
            entries[2].insert(0, str(match))

    mu_cb_label = tk.Label(frame, text="Material (μᵣ)", bg="white", anchor="w")
    mu_cb_label.grid(row=3, column=3, sticky="w", padx=10, pady=(5, 0))

    mu_cb = ttk.Combobox(frame, values=[mat for _, mat in mu_table], width=20)
    mu_cb.grid(row=4, column=3, padx=10, pady=(5, 0))
    mu_cb.bind("<<ComboboxSelected>>", on_mu_select)

    # --- Conductance ComboBox --------------
    def on_cond_select(event):
        selected = cond_cb.get()
        match = next((v for v, mat in conductance_table if mat == selected), None)
        if match is not None:
            entries[4].delete(0, tk.END)
            entries[4].insert(0, str(match))

    cond_cb_label = tk.Label(frame, text="Material (ϰ)", bg="white", anchor="w")
    cond_cb_label.grid(row=5, column=3, sticky="w", padx=10, pady=(5, 0))

    cond_cb = ttk.Combobox(frame, values=[mat for _, mat in conductance_table], width=20)
    cond_cb.current(0)
    cond_cb.grid(row=6, column=3, padx=10, pady=(5, 0))
    cond_cb.bind("<<ComboboxSelected>>", on_cond_select)

    # --- Result Output ---------------------
    result_label = tk.Label(frame, text="Inductance L", bg="white", anchor="w")
    result_label.grid(row=12, column=0, sticky="w", padx=10, pady=(15, 5))

    result_var = tk.StringVar()
    result_entry = tk.Entry(frame, textvariable=result_var, width=20, state="readonly")
    result_entry.grid(row=12, column=1, padx=10, pady=(15, 5))

    ttk.Combobox(frame, values=list(unit_factors_inductance.keys()), width=5,
                 textvariable=output_unit_var, state="readonly").grid(row=12, column=2, padx=(2, 0), pady=(15, 5))

    precision_label = tk.Label(frame, text="Error < 5%", bg="white", anchor="w")
    precision_label.grid(row=12, column=3, sticky="w", padx=10, pady=5)
    # --- Calculate Button ------------------
    def calculate():
        try:
            s = float(entries[0].get())*100*unit_factors_length[sidelength_unit_var.get()] #m->cm
            d = float(entries[1].get())*100*unit_factors_length[diameter_unit_var.get()]#m->cm
            mu = float(entries[2].get())
            f = float(entries[3].get())*unit_factors_frequency[frequency_unit_var.get()]
            kappa = float(entries[4].get())
            delta = hertwig_skineffekt(f,kappa,d)
            inductance =  (8*s*(np.log(2*s/d)+d/(2*s)-0.774+mu*delta))*10**(-9)* unit_factors_inductance[output_unit_var.get()]
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
        text=r"Harry Hertwig: Induktivitäten. Berlin: Verlag für Radio-Foto-Kinotechnik. 1954. Induktivität einer quardratischen Drahtschleife aus Runddraht.",
        bg="white",
        font=("Arial", 10),
        fg="gray"
    )
    footer.grid(row=15, column=0, columnspan=9, pady=(10, 10))

    return frame