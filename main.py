import tkinter as tk
import pathlib, os
import importlib
from PIL import Image, ImageTk
from collections import defaultdict

dir_path = os.path.dirname(os.path.realpath(__file__))
current_dir = pathlib.Path(__file__).parent.resolve()

# -------------------------- DEFINING THE COLORS -------------------------
selectionbar_color = '#eff5f6'
sidebar_color = "#FDE1E1"
header_color = "#850303"
visualisation_frame_color = "#ffffff"

# -------------------------- BEGIN APP -----------------------------------

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("1100x700")
        self.resizable(1, 1)
        self.title("EEECal")
        self.config(background=selectionbar_color)
        self.icon = tk.PhotoImage(file=os.path.join(current_dir, "icon.png"))
        self.iconphoto(True, self.icon)

        # ---------------- HEADER ----------------------------------------

        self.header_frame = tk.Frame(self, bg=header_color, highlightbackground="#808080", highlightthickness=0.5)
        self.header_frame.place(relx=0.3, rely=0, relwidth=0.7, relheight=0.1)
        self.header_label = tk.Label(
            self.header_frame,
            text="EEECal",
            font=("Arial", 18),
            bg=header_color,
            fg="white",
            wraplength=600,
            justify="center"
        )
        self.header_label.pack(pady=10, fill=tk.BOTH, expand=True)

        # ---------------- SIDEBAR ---------------------------------------

        self.sidebar_frame = tk.Frame(self, bg=sidebar_color, highlightbackground="#808080", highlightthickness=0.5)
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

        self.sidebar_canvas.bind_all("<MouseWheel>", lambda event: self.sidebar_canvas.yview_scroll(-1 * int(event.delta / 120), "units"))


        # -------------------- MAIN FRAME --------------------------------
        # Scrollable

        self.main_container = tk.Frame(self, bg="white", highlightbackground="#808080", highlightthickness=0.5)
        self.main_container.place(relx=0.3, rely=0.1, relwidth=0.7, relheight=0.9)

        self.main_canvas = tk.Canvas(self.main_container, bg="white", highlightthickness=0)
        self.main_scrollbar = tk.Scrollbar(self.main_container, orient="vertical", command=self.main_canvas.yview)
        self.main_scrollable_frame = tk.Frame(self.main_canvas, bg="white")

        self.main_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(
                scrollregion=self.main_canvas.bbox("all")
            )
        )

        self.main_canvas.create_window((0, 0), window=self.main_scrollable_frame, anchor="nw")
        self.main_canvas.configure(yscrollcommand=self.main_scrollbar.set)

        self.main_canvas.pack(side="left", fill="both", expand=True)
        self.main_scrollbar.pack(side="right", fill="y")

        self.main_canvas.bind_all("<MouseWheel>", lambda event: self.main_canvas.yview_scroll(-1 * int(event.delta / 120), "units"))

        # -------------------- INIT --------------------------------------
        self.create_header()
        self.load_modules()
        self.create_brand_frame()
        self.create_sidebar()

        # Load default module
        default_module = "dashboard.home"
        if default_module in self.module_paths:
            index = self.module_paths.index(default_module)
            self.load_module(index)
        else:
            print("Default module not found.")

# --------------- FUNCTION DEFINITIONS -----------------------------------

    #self-explanatory
    def create_header(self):
        label = tk.Label(self.header_frame, text="EEECal", font=("Arial", 18), bg=header_color)
        label.pack(pady=10)

    #loads the modules and the subfolders
    def load_modules(self):
        self.module_names = []
        self.module_paths = []
        self.subfolder_names = []
        self.subfolder_paths = []

        self.subfolder_paths = [f.path for f in os.scandir(dir_path) if f.is_dir() and f.name != "__pycache__" and f.name != "images"]

        for path in self.subfolder_paths:
            self.subfolder_names.append(os.path.basename(path))

        self.i = 0
        for subfolder in self.subfolder_paths:
            folder_name = self.subfolder_names[self.i]
            for file in os.listdir(os.path.join(dir_path, folder_name)):
                if file.endswith(".py") and not file.startswith("__"):
                    name = file[:-3]
                    if (folder_name == "dashboard" and name != "home") or (folder_name == "addresources"):
                        continue
                    self.module_names.append(name)
                    self.module_paths.append(f"{folder_name}.{name}")
            self.i += 1

    # generates the sidemenu
    def create_sidebar(self):
        modules_by_folder = defaultdict(list)
        for path in self.module_paths:
            folder, mod = path.split(".")
            modules_by_folder[folder].append((mod, path))

        default_module = "dashboard.home"      #makes the home button in the top position
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
                wraplength=230,
                justify="left"
            )
            home_button.pack(fill=tk.X, padx=10, pady=(5, 15))

        # generates the other sidemenu entries
        for folder_name in self.subfolder_names:
            if folder_name == "dashboard" and "home" in [m[0] for m in modules_by_folder[folder_name]]:
                modules_by_folder[folder_name] = [m for m in modules_by_folder[folder_name] if m[0] != "home"]

            if not modules_by_folder[folder_name]:
                continue

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
                    wraplength=230,
                    justify="left"
                )
                button.pack(fill=tk.X, padx=20, pady=2)

    # makes the logo and name
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

    #loads modul in the mainframe
    def load_module(self, index):
        # Clear previous widgets
        for widget in self.main_scrollable_frame.winfo_children():
            widget.destroy()

        module_name = self.module_paths[index]
        visible_name = self.module_names[index].capitalize()
        self.header_label.config(text=visible_name)
        try:
            module = importlib.import_module(module_name)
            importlib.reload(module)
            frame = module.create_frame(self.main_scrollable_frame)
            frame.pack(fill=tk.BOTH, expand=True)
        except Exception as e:
            print(f"Error loading module '{module_name}': {e}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
