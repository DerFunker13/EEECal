import os
module_names = []
module_paths = []

dir_path = os.path.dirname(os.path.realpath(__file__))





module_names = []
module_paths = []
subfolder_names = []
subfolder_paths = []

subfolder_paths = [f.path for f in os.scandir(dir_path) if f.is_dir() and f.name != "__pycache__" and f.name != "images"]

for path in subfolder_paths:
    subfolder_names.append(os.path.basename(path))


for subfolder in subfolder_paths:
    for file in os.listdir(subfolder):
        if file.endswith(".py") and not file.startswith("__"):
            name = file[:-3]
            module_names.append(name)
            module_paths.append(f"{os.path.basename(subfolder)}.{name}")

    
print(module_names)
print(module_paths)  
print(subfolder_names)
print(subfolder_paths)


def create_sidebar(self):

        for i, module_name in enumerate(self.module_names):
            button = tk.Button(
                self.sidebar_frame,
                text=module_name.capitalize(),
                command=lambda i=i: self.load_module(i),
                anchor="w"
            )
            button.pack(fill=tk.X, padx=5, pady=5)