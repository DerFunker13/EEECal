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
    title_label = tk.Label(frame, text="Self-Inductance of a circular ring with tubular cross-section", font=("Arial", 16, "bold"), bg="white")
    title_label.grid(row=0, column=0, columnspan=8, sticky="w", padx=10, pady=10)

    # --- Image (Top-Right) ----------------
    image_path = os.path.join(os.path.dirname(__file__), "pic_rohr ring.jpg")
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
    labels = ["Diameter D", "inner tubular diameter d₁", "outer tubular diameter d₂"]
    entries = []
    default_values = ["50","5","10"]

    diameter_unit_var = tk.StringVar(value="cm")
    indiameter_unit_var = tk.StringVar(value="mm")
    outdiameter_unit_var = tk.StringVar(value="mm")
    output_unit_var = tk.StringVar(value="H")

    for i, text in enumerate(labels):
        lbl = tk.Label(frame, text=text, bg="white", anchor="w")
        lbl.grid(row=i+2, column=0, sticky="w", padx=10, pady=5)

        ent = tk.Entry(frame, width=30, textvariable=tk.StringVar(value=default_values[i]))
        ent.grid(row=i+2, column=1, padx=10, pady=5)
        entries.append(ent)

        if i == 0:
            ttk.Combobox(frame, values=list(unit_factors_length.keys()), width=5, state="readonly",
                         textvariable=diameter_unit_var).grid(row=i + 2, column=2, padx=(2, 0))
        elif i == 1:
            ttk.Combobox(frame, values=list(unit_factors_length.keys()), width=5, state="readonly",
                         textvariable=indiameter_unit_var).grid(row=i + 2, column=2, padx=(2, 0))
        elif i == 2:
            ttk.Combobox(frame, values=list(unit_factors_length.keys()), width=5, state="readonly",
                         textvariable=outdiameter_unit_var).grid(row=i + 2, column=2, padx=(2, 0))
            
    # --- Result Output 1 ---------------------
    result_label1 = tk.Label(frame, text="Inductance L₀(low. freq.)(H)", bg="white", anchor="w")
    result_label1.grid(row=12, column=0, sticky="w", padx=10, pady=(15, 5))

    result_var1 = tk.StringVar()
    result_entry1 = tk.Entry(frame, textvariable=result_var1, width=30, state="readonly")
    result_entry1.grid(row=12, column=1, padx=10, pady=(15, 5))

    precision_label1 = tk.Label(frame, text="Error < 5%", bg="white", anchor="w")
    precision_label1.grid(row=12, column=3, sticky="w", padx=10, pady=5)

    ttk.Combobox(frame, values=list(unit_factors_inductance.keys()), width=5,
                 textvariable=output_unit_var, state="readonly").grid(row=12, column=2, padx=(2, 0), pady=(15, 5))
    
    # --- Result Output 2 ---------------------
    result_label2 = tk.Label(frame, text="Inductance L ͚ (high. freq.)(H)", bg="white", anchor="w")
    result_label2.grid(row=13, column=0, sticky="w", padx=10, pady=(5, 5))

    result_var2 = tk.StringVar()
    result_entry2 = tk.Entry(frame, textvariable=result_var2, width=30, state="readonly")
    result_entry2.grid(row=13, column=1, padx=10, pady=(5, 5))

    #precision_label2 = tk.Label(frame, text="Error < 5%", bg="white", anchor="w")
    #precision_label2.grid(row=13, column=2, sticky="w", padx=10, pady=5)
    # --- Calculate Button ------------------
    def calculate():
        try:
            D = float(entries[0].get())*100*unit_factors_length[diameter_unit_var.get()] #m->cm
            d1 = float(entries[1].get())*100*unit_factors_length[indiameter_unit_var.get()] #m->cm
            d2 = float(entries[2].get())*100*unit_factors_length[outdiameter_unit_var.get()] #m->cm
            
            if d1 >= d2:
                result_var1.set("Invalid input!")
                result_var2.set("Invalid input!")

            inductance_low = (2*np.pi*D*(np.log(8*D/d2)-1.75-(d1**2)/(2*(d2**2-d1**2))+(d1**4)*np.log(d2/d1)/(2*(d2**2-d1**2))))*10**(-9)* unit_factors_inductance[output_unit_var.get()]
            inductance_high = (2*np.pi*D*(np.log(8*D/d2)-2))*10**(-9)* unit_factors_inductance[output_unit_var.get()]
            result_var1.set(f"{inductance_low:.4e}")
            result_var2.set(f"{inductance_high:.4e}")
        except ValueError:
            result_var1.set("Invalid input!")
            result_var2.set("Invalid input!")

    calc_button = tk.Button(frame, text="Calculate", command=calculate, bg="#e1e1e1")
    calc_button.grid(row=14, column=0, columnspan=2, pady=(10, 5))

    
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
        text=r"Harry Hertwig: Induktivitäten. Berlin: Verlag für Radio-Foto-Kinotechnik. 1954. Induktivität eines Kreisringes mit rohrförmigem Querschnitt.",
        bg="white",
        font=("Arial", 10),
        fg="gray"
    )
    footer.grid(row=15, column=0, columnspan=8, pady=(10, 10))

    return frame