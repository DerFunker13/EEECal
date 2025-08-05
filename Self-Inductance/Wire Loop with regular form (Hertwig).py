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

form_table = [
    (2.451,"Circle"),
    (2.561,"Regular octagon"),
    (2.636,"Regular hexagon"),
    (2.712,"Regular pentagon"),   
    (2.853,"Square"),
    (3.332,"Isosceles right-angled triangle"),
    (3.197,"Isosceles triangle"),
]

def create_frame(parent):
    frame = tk.Frame(parent, bg="white")

    # --- Title -----------------------------
    title_label = tk.Label(frame, text="Self-Inductance of a Wire Loop with regular form (high freq.)", font=("Arial", 16, "bold"), bg="white")
    title_label.grid(row=0, column=0, columnspan=3, sticky="w", padx=10, pady=10)

    # --- Image (Top-Right) ----------------
    image_path = os.path.join(os.path.dirname(__file__), "pic_rectangular Wire Loop with regular form.jpg")
    try:
        image = Image.open(image_path)
        image = image.resize((250, 200))
        photo = ImageTk.PhotoImage(image)
        image_label = tk.Label(frame, image=photo, bg="white")
        image_label.image = photo
        image_label.grid(row=2, column=2, rowspan=12, sticky="ne")
    except Exception as e:
        print("Image load error:", e)

    # --- Entry Fields ---------------------
    labels = ["Circumference l (m)", "Conductor diameter d (m)"]
    entries = []
    default_values = ["120e-2","1e-2"]

    for i, text in enumerate(labels):
        lbl = tk.Label(frame, text=text, bg="white", anchor="w")
        lbl.grid(row=i+2, column=0, sticky="w", padx=10, pady=5)

        ent = tk.Entry(frame, width=30, textvariable=tk.StringVar(value=default_values[i]))
        ent.grid(row=i+2, column=1, padx=10, pady=5)
        entries.append(ent)

    # --- Form ComboBox --------------

    form_cb_label = tk.Label(frame, text="Form", bg="white", anchor="w")
    form_cb_label.grid(row=4, column=0, sticky="w", padx=10, pady=(5, 0))

    form_cb = ttk.Combobox(frame, values=[mat for _, mat in form_table], width=28)
    #form_cb.current(0)
    form_cb.grid(row=4, column=1, padx=10, pady=(5, 0))
    form_cb.bind("<<ComboboxSelected>>")

    # --- Result Output ---------------------
    result_label = tk.Label(frame, text="Inductance L ͚ (H)", bg="white", anchor="w")
    result_label.grid(row=12, column=0, sticky="w", padx=10, pady=(15, 5))

    result_var = tk.StringVar()
    result_entry = tk.Entry(frame, textvariable=result_var, width=30, state="readonly")
    result_entry.grid(row=12, column=1, padx=10, pady=(15, 5))

    precision_label = tk.Label(frame, text="Error ≈ 0.5%", bg="white", anchor="w")
    precision_label.grid(row=12, column=2, sticky="w", padx=5, pady=5)

    # --- Calculate Button ------------------
    def form_select():
        selected = form_cb.get()
        match = next((v for v, mat in form_table if mat == selected), None)
        return match
    def calculate():
        try:
            l = float(entries[0].get())*100 #m->cm
            d = float(entries[1].get())*100 #m->cm
            formfactor = float(form_select())
            ind1 = 2*l*(np.log(4*l/d)-formfactor)
            inductance =  (ind1)*10**(-9)
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
        text=r"Harry Hertwig: Induktivitäten. Berlin: Verlag für Radio-Foto-Kinotechnik. 1954. Induktivität einer rechteckigen Drahtschleife mit rechteckigem Leiterquerschnitt.",
        bg="white",
        font=("Arial", 10),
        fg="gray"
    )
    footer.grid(row=15, column=0, columnspan=3, pady=(10, 10))

    return frame