import tkinter as tk
import pathlib, os
import importlib
dir_path = os.path.dirname(os.path.realpath(__file__))
current_dir = pathlib.Path(__file__).parent.resolve()
from PIL import Image, ImageTk

from collections import defaultdict
# -------------------------- DEFINING THE COLORS -------------------------

selectionbar_color = '#eff5f6'
sidebar_color = "#FDE1E1"
header_color = "#850303"
visualisation_frame_color = "#ffffff"




class App(tk.Tk):
    def __init__(self):
        super().__init__()

        
        self.geometry("1100x700")
        self.resizable(1, 1)
        self.title("EEECal")
        self.config(background=selectionbar_color)
        self.icon = tk.PhotoImage(file=os.path.join(current_dir, "icon.png"))
        self.iconphoto(True, self.icon)

        # Layout setup

        # ---------------- HEADER ------------------------

        self.header_frame = tk.Frame(self, bg=header_color)
        self.header_frame.config(
            highlightbackground="#808080",
            highlightthickness=0.5
        )
        self.header_frame.place(relx=0.3, rely=0, relwidth=0.7, relheight=0.1)
        self.header_label = tk.Label(
            self.header_frame,
            text="EEECal",
            font=("Arial", 18),
            bg=header_color,
            fg="white",
            wraplength=600,     # Adjust this to fit your layout width
            justify="center"
        )
        self.header_label.pack(pady=10, fill=tk.BOTH, expand=True)

        # ---------------- SIDEBAR -----------------------

        self.sidebar_frame = tk.Frame(self, bg=sidebar_color)
        self.sidebar_frame.config(
            highlightbackground="#808080",
            highlightthickness=0.5
            )
        self.sidebar_frame.place(relx=0, rely=0, relwidth=0.3, relheight=1)

        # Scrollable sidebar setup
        self.sidebar_canvas = tk.Canvas(self.sidebar_frame, bg=sidebar_color, highlightthickness=0)
        self.sidebar_scrollbar = tk.Scrollbar(self.sidebar_frame, orient="vertical", command=self.sidebar_canvas.yview)
        self.sidebar_scrollable_frame = tk.Frame(self.sidebar_canvas, bg=sidebar_color)

        self.sidebar_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.sidebar_canvas.configure(
                scrollregion=self.sidebar_canvas.bbox("all")
            )
        )

        self.sidebar_canvas.create_window((0, 0), window=self.sidebar_scrollable_frame, anchor="nw")
        self.sidebar_canvas.configure(yscrollcommand=self.sidebar_scrollbar.set)

        self.sidebar_canvas.pack(side="left", fill="both", expand=True)
        self.sidebar_scrollbar.pack(side="right", fill="y")
        #Scrolleble

        self.sidebar_canvas.bind_all("<MouseWheel>", lambda event: self.sidebar_canvas.yview_scroll(-1 * int(event.delta / 120), "units"))

        #def _on_mousewheel(event):
        #    self.sidebar_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        #self.sidebar_canvas.bind("<Enter>", lambda e: self.sidebar_canvas.bind_all("<MouseWheel>", _on_mousewheel))
        #self.sidebar_canvas.bind("<Leave>", lambda e: self.sidebar_canvas.unbind_all("<MouseWheel>"))


        # --------------------  MULTI PAGE SETTINGS ----------------------------

        self.main_frame = tk.Frame(self, bg="white")
        #self.main_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        self.main_frame.config(highlightbackground="#808080", highlightthickness=0.5)
        self.main_frame.place(relx=0.3, rely=0.1, relwidth=0.7, relheight=0.9)

        self.create_header()
        self.load_modules()
        self.create_brand_frame()
        self.create_sidebar()


        # ✅ Automatically load the first module (e.g. "home")
        default_module = "dashboard.home"  # <--- folder.module
        if default_module in self.module_paths:
            index = self.module_paths.index(default_module)
            self.load_module(index)
        else:
            print("Default module not found.")

    def create_header(self):
        label = tk.Label(self.header_frame, text="EEECal", font=("Arial", 18), bg=header_color)
        label.pack(pady=10)

    def load_modules(self):
        self.module_names = []
        self.module_paths = []
        self.subfolder_names = []
        self.subfolder_paths = []

        self.subfolder_paths = [f.path for f in os.scandir(dir_path) if f.is_dir() and f.name != "__pycache__" and f.name != "images"]

        for path in self.subfolder_paths:
            self.subfolder_names.append(os.path.basename(path))

        self.i=0
        for subfolder in self.subfolder_paths:
            folder_name = self.subfolder_names[self.i]
            for file in os.listdir(dir_path+"\\" + self.subfolder_names[self.i]):
                if file.endswith(".py") and not file.startswith("__"):
                    name = file[:-3]
                    if folder_name == "dashboard" and name != "home":
                        continue
                    #print(name)
                    self.module_names.append(name)
                    self.module_paths.append(f"{os.path.basename(subfolder)}.{name}")
            self.i=self.i+1
        
        #print(self.module_paths)

    def create_sidebar(self):
        from collections import defaultdict

        # Organize modules by subfolder
        modules_by_folder = defaultdict(list)
        for path in self.module_paths:
            folder, mod = path.split(".")
            modules_by_folder[folder].append((mod, path))

        # --- Step 1: Always show "Home" at the top
        default_module = "dashboard.home"
        if default_module in self.module_paths:
            index = self.module_paths.index(default_module)
            home_button = tk.Button(
                self.sidebar_scrollable_frame,
                text="Home",
                command=lambda i=index: self.load_module(i),
                anchor="w",
                relief=tk.FLAT,
                bg=sidebar_color,
                activebackground="#D9B8F7",
                font=("Arial", 12, "bold"),
                wraplength=230,     # Adjust for padding/margin
                justify="left"
            )
            home_button.pack(fill=tk.X, padx=10, pady=(5, 15))  # Padding to separate from the rest

        # --- Step 2: Show all other modules, skipping "dashboard.home"
        for folder_name in self.subfolder_names:
            if folder_name == "dashboard" and "home" in [m[0] for m in modules_by_folder[folder_name]]:
                # Remove "home" from dashboard to avoid duplicate
                modules_by_folder[folder_name] = [m for m in modules_by_folder[folder_name] if m[0] != "home"]

            if not modules_by_folder[folder_name]:
                continue

            # Folder label
            folder_label = tk.Label(
                self.sidebar_scrollable_frame,
                text=folder_name,
                bg=sidebar_color,
                fg="black",
                font=("Arial", 12, "bold"),
                anchor="w",
                wraplength=250,
                justify="left"
            )
            folder_label.pack(fill=tk.X, padx=10, pady=(10, 0))

            for mod_name, full_path in modules_by_folder[folder_name]:
                idx = self.module_paths.index(full_path)
                button = tk.Button(
                    self.sidebar_scrollable_frame,
                    text=f"  {mod_name}",
                    command=lambda i=idx: self.load_module(i),
                    anchor="w",
                    relief=tk.FLAT,
                    bg=sidebar_color,
                    activebackground="#D9B8F7",
                    wraplength=230,     # Adjust for padding/margin
                    justify="left"
                )
                button.pack(fill=tk.X, padx=20, pady=2)
        

    #----------------- Brandframe ---------------------

    def create_brand_frame(self):
        self.brand_frame = tk.Frame(self.sidebar_scrollable_frame, bg=sidebar_color)
        self.brand_frame.pack(fill=tk.X, padx=10, pady=10)
        self.prg_logo = self.icon.subsample(9)
        logo = tk.Label(self.brand_frame, image=self.prg_logo, bg=sidebar_color)
        logo.pack(side=tk.LEFT, padx=5)

        prg_name = tk.Label(self.brand_frame,
                            text='EEECal',
                            bg=sidebar_color,
                            font=("Arial", 15, "bold"))
        prg_name.pack(side=tk.LEFT, padx=10)

    def load_module(self, index):
        # Clear previous widgets
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        module_name = self.module_paths[index]
        visible_name = self.module_names[index].capitalize()
        self.header_label.config(text=visible_name)
        try:
            module = importlib.import_module(module_name)
            importlib.reload(module)  # Optional: for development
            frame = module.create_frame(self.main_frame)
            frame.pack(fill=tk.BOTH, expand=True)
        except Exception as e:
            print(f"Error loading module '{module_name}': {e}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
