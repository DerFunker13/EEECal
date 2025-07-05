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



def create_frame(parent):
    frame = tk.Frame(parent, bg="white")

    # ─── Title ─────────────────────────────
    title_label = tk.Label(frame, text="Self-Inductance of a Round Magnetic Conductor", font=("Arial", 16, "bold"), bg="white")
    title_label.grid(row=0, column=0, columnspan=5, sticky="w", padx=10, pady=10)

    # ─── Image (Top-Right) ────────────────
    image_path = os.path.join(os.path.dirname(__file__), "pic_long round conductor.png")
    try:
        image = Image.open(image_path)
        image = image.resize((200, 250))
        photo = ImageTk.PhotoImage(image)
        image_label = tk.Label(frame, image=photo, bg="white")
        image_label.image = photo
        image_label.grid(row=1, column=3, rowspan=10, sticky="ne", padx=10, pady=10)
    except Exception as e:
        print("Image load error:", e)

    # ─── Entry Fields ─────────────────────
    labels = ["Length l (m)", "Diameter d (m)", "rel. Permeability μᵣ", "Frequency f (Hz)", "Conductance ϰ (S/m)"]
    entries = []
    default_values = ["3","5e-3","1","0","59600000.0"]

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
            entries[2].delete(0, tk.END)
            entries[2].insert(0, str(match))

    mu_cb_label = tk.Label(frame, text="Material (μᵣ)", bg="white", anchor="w")
    mu_cb_label.grid(row=3, column=2, sticky="w", padx=10, pady=(5, 0))

    mu_cb = ttk.Combobox(frame, values=[mat for _, mat in mu_table], width=28)
    mu_cb.grid(row=4, column=2, padx=10, pady=(5, 0))
    mu_cb.bind("<<ComboboxSelected>>", on_mu_select)

    # ─── Conductance ComboBox ──────────────
    def on_cond_select(event):
        selected = cond_cb.get()
        match = next((v for v, mat in conductance_table if mat == selected), None)
        if match is not None:
            entries[4].delete(0, tk.END)
            entries[4].insert(0, str(match))

    cond_cb_label = tk.Label(frame, text="Material (ϰ)", bg="white", anchor="w")
    cond_cb_label.grid(row=5, column=2, sticky="w", padx=10, pady=(5, 0))

    cond_cb = ttk.Combobox(frame, values=[mat for _, mat in conductance_table], width=28)
    cond_cb.current(0)
    cond_cb.grid(row=6, column=2, padx=10, pady=(5, 0))
    cond_cb.bind("<<ComboboxSelected>>", on_cond_select)

    # ─── Result Output ─────────────────────
    result_label = tk.Label(frame, text="Inductance (H)", bg="white", anchor="w")
    result_label.grid(row=9, column=0, sticky="w", padx=10, pady=(15, 5))

    result_var = tk.StringVar()
    result_entry = tk.Entry(frame, textvariable=result_var, width=30, state="readonly")
    result_entry.grid(row=9, column=1, padx=10, pady=(15, 5))

    precision_label = tk.Label(frame, text="Error < 5%", bg="white", anchor="w")
    precision_label.grid(row=9, column=2, sticky="w", padx=10, pady=5)
    # ─── Calculate Button ──────────────────
    def calculate():
        try:
            l = float(entries[0].get())
            d = float(entries[1].get())
            mu_r = float(entries[2].get())
            f = float(entries[3].get())
            kappa = float(entries[4].get())
            delta = hertwig_skineffekt(f,kappa,d)
            #print(delta)
            inductance = 2 * l * 100 * (np.log(4 * l / d) - 1 + (mu_r * delta)) * 10 ** -9
            result_var.set(f"{inductance:.4e}")
        except ValueError:
            result_var.set("Invalid input!")

    calc_button = tk.Button(frame, text="Calculate", command=calculate, bg="#e1e1e1")
    calc_button.grid(row=10, column=0, columnspan=2, pady=(10, 5))

    
    # ─── Text ────────────────────────────
#    text = tk.Text(
#        frame,
#        bg="white",
#        font=("Arial", 12),
#        fg="gray"
#    )
#    text.grid(row=11, column=0, columnspan=4, pady=(10, 10))
#    
#    quote = """ """
#    text.insert("1.0",quote)
    
    # ─── Footer ────────────────────────────
    footer = tk.Label(
        frame,
        text=r"Harry Hertwig: Induktivitäten. Berlin: Verlag für Radio-Foto-Kinotechnik. 1954. Selbstinduktivität eines gestreckten Rundleiters",
        bg="white",
        font=("Arial", 10),
        fg="gray"
    )
    footer.grid(row=12, column=0, columnspan=3, pady=(10, 10))

    return frame
