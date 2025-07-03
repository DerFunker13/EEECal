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

P2hl=[
    [0.0,   0.1,   0.2,   0.3,   0.4,   0.5,   0.6,   0.7,   0.8,   0.9,   1.0],
    [0.0000,0.0975,0.1900,0.2778,0.3608,0.4393,0.5136,0.5840,0.6507,0.7139,0.7740],
]

Q2lh=[
    [0.0,   0.1,   0.2,   0.3,   0.4,   0.5,
     0.6,   0.7,   0.8,   0.9,   1.0],
    [1.0000,1.0499,1.0997,1.1489,1.1975,1.2452,
     1.2918,1.3373,1.3819,1.4251,1.4672],
]

kn=[
    [2,3,    4,    5,    6,   7,   8,   9,   10,  11,  12,  13,  14,  15,  16,  17,  18,  19,  20],
    [0,0.308,0.621,0.906,1.18,1.43,1.66,1.86,2.05,2.22,2.37,2.51,2.63,2.74,2.85,2.95,3.04,3.14,3.24],
]




def create_frame(parent):
    frame = tk.Frame(parent, bg="white")

    # ─── Title ─────────────────────────────
    title_label = tk.Label(frame, text="Self-Inductance of multiple Conductors against Earth", font=("Arial", 16, "bold"), bg="white")
    title_label.grid(row=0, column=0, columnspan=3, sticky="w", padx=10, pady=10)

    # ─── Image (Top-Right) ────────────────
    image_path = os.path.join(os.path.dirname(__file__), "pic_multiple conductors against earth.jpg")
    try:
        image = Image.open(image_path)
        image = image.resize((200, 125))
        photo = ImageTk.PhotoImage(image)
        image_label = tk.Label(frame, image=photo, bg="white")
        image_label.image = photo
        image_label.grid(row=1, column=3, rowspan=10, sticky="ne", padx=10, pady=10)
    except Exception as e:
        print("Image load error:", e)

    # ─── Entry Fields ─────────────────────
    labels = ["Length l (m)", "Diameter d (m)", "Distance between conductors a (m)", "Distance to earth h (m)","Number of conductors n","rel. Permeability μᵣ", "Frequency f (Hz)", "Conductance ϰ (S/m)"]
    entries = []
    default_values = ["3","5e-3","25e-2","25e-2","2","1","0","59600000.0"]

    for i, text in enumerate(labels):
        lbl = tk.Label(frame, text=text, bg="white", anchor="w")
        lbl.grid(row=i+2, column=0, sticky="w", padx=10, pady=5)

        ent = tk.Entry(frame, width=30, textvariable=tk.StringVar(value=default_values[i]))
        ent.grid(row=i+2, column=1, padx=10, pady=5)
        entries.append(ent)

    # ─── Permeability ComboBox ─────────────
    def on_mu_select(event):
        selected = mu_cb.get()
        match = next((v for v, mat in mu_table if mat == selected), None)
        if match is not None:
            entries[5].delete(0, tk.END)
            entries[5].insert(0, str(match))

    mu_cb_label = tk.Label(frame, text="Material (μᵣ)", bg="white", anchor="w")
    mu_cb_label.grid(row=6, column=2, sticky="w", padx=10, pady=(5, 0))

    mu_cb = ttk.Combobox(frame, values=[mat for _, mat in mu_table], width=28)
    mu_cb.grid(row=7, column=2, padx=10, pady=(5, 0))
    mu_cb.bind("<<ComboboxSelected>>", on_mu_select)

    # ─── Conductance ComboBox ──────────────
    def on_cond_select(event):
        selected = cond_cb.get()
        match = next((v for v, mat in conductance_table if mat == selected), None)
        if match is not None:
            entries[7].delete(0, tk.END)
            entries[7].insert(0, str(match))

    cond_cb_label = tk.Label(frame, text="Material (σ)", bg="white", anchor="w")
    cond_cb_label.grid(row=8, column=2, sticky="w", padx=10, pady=(5, 0))

    cond_cb = ttk.Combobox(frame, values=[mat for _, mat in conductance_table], width=28)
    cond_cb.current(0)
    cond_cb.grid(row=9, column=2, padx=10, pady=(5, 0))
    cond_cb.bind("<<ComboboxSelected>>", on_cond_select)

    # ─── Result Output ─────────────────────
    result_label = tk.Label(frame, text="Inductance (H)", bg="white", anchor="w")
    result_label.grid(row=12, column=0, sticky="w", padx=10, pady=(15, 5))

    result_var = tk.StringVar()
    result_entry = tk.Entry(frame, textvariable=result_var, width=30, state="readonly")
    result_entry.grid(row=12, column=1, padx=10, pady=(15, 5))

    precision_label = tk.Label(frame, text="Error ≈ 1%", bg="white", anchor="w")
    precision_label.grid(row=12, column=2, sticky="w", padx=10, pady=5)
    # ─── Calculate Button ──────────────────
    def calculate():
        try:
            l = float(entries[0].get())*100 #m->cm
            d = float(entries[1].get())*100 #m->cm
            a = float(entries[2].get())*100 #m->cm
            h = float(entries[3].get())*100 #m->cm
            n = float(entries[4].get())
            mu_r = float(entries[5].get())
            f = float(entries[6].get())
            kappa = float(entries[7].get())
            delta = hertwig_skineffekt(f,kappa,d)
            #print(delta)
            if 2*h<l:
                (flag, P)=interpolate(P2hl[0], P2hl[1], (2*h/l))
                M=2*l*(np.log(2*h/a-P+a/l))* 10**(-9)
            else:
                (flag, Q)=interpolate(Q2lh[0], Q2lh[1], (l/(2*h)))
                M=2*l*(np.log(2*l/a-Q+a/l))* 10**(-9)
            if flag==1:
                result_var.set("Invalid input!")
            if n<2 or n>20:
                result_var.set("n must be between 2 and 20!")
            L1 =  (2*l*(np.log((l+np.sqrt(l**2 + d**2 /4))/(l+np.sqrt(l**2 + 4 * h**2)))+np.log(4*h/d)) + 2*(np.sqrt(l**2 + 4 * h**2)-np.sqrt(l**2 + d**2 /4)+ mu_r*delta*l-2*h+(d/2)))* 10**(-9)
            
            inductance =  (((L1+(n-1)*M)/n)-kn[int(n)-2])
            result_var.set(f"{inductance:.4e}")
        except ValueError:
            result_var.set("Invalid input!")

    calc_button = tk.Button(frame, text="Calculate", command=calculate, bg="#e1e1e1")
    calc_button.grid(row=13, column=0, columnspan=2, pady=(10, 5))

    
    # ─── Text ────────────────────────────
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
    
    # ─── Footer ────────────────────────────
    footer = tk.Label(
        frame,
        text=r"Harry Hertwig: Induktivitäten. Berlin: Verlag für Radio-Foto-Kinotechnik. 1954. Induktivität eines Leiters gegen Erde.",
        bg="white",
        font=("Arial", 10),
        fg="gray"
    )
    footer.grid(row=15, column=0, columnspan=3, pady=(10, 10))

    return frame