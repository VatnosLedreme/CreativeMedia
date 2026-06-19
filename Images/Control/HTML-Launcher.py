import os
import sys
import tkinter as tk
import webbrowser
import subprocess

# --- CONFIGURATION ---
# We strictly resolve the base directory to avoid arbitrary path traversal
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECTS_DIR = os.path.join(BASE_DIR, "projects")

def generate_html_icon():
    """
    Procedurally generates a 32x32 pixel HTML/Web Launcher icon in PPM format.
    This creates a dark browser window with a vibrant orange play button.
    This procedural approach is entirely safe and avoids dropping hidden image files.
    """
    ppm = ["P3\n32 32\n255\n"]
    for y in range(32):
        for x in range(32):
            if 2 <= y <= 29 and 2 <= x <= 29:
                if y <= 7: 
                    # Top bar dots
                    if 4 <= x <= 6 and 4 <= y <= 5: 
                        ppm.append("255 95 86 ")
                    elif 9 <= x <= 11 and 4 <= y <= 5: 
                        ppm.append("255 189 46 ")
                    elif 14 <= x <= 16 and 4 <= y <= 5: 
                        ppm.append("39 201 63 ")
                    else: 
                        ppm.append("45 45 45 ")
                else:
                    # Main window body and play triangle
                    if 10 <= x <= 22 and abs(y - 18) <= (22 - x) * 0.8:
                        ppm.append("228 77 38 ")
                    else:
                        ppm.append("30 30 30 ")
            else:
                ppm.append("20 20 20 ")
        ppm.append("\n")
        
    return "".join(ppm)

class LauncherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HTML Project Launcher")
        self.root.geometry("320x450")
        self.root.configure(bg="#1e1e1e")

        # --- SET SAFE PROCEDURAL ICON ---
        # Look for a physical .ico file first (for the Windows Taskbar)
        icon_path = os.path.join(BASE_DIR, "app_icon.ico")
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except Exception:
                pass
        else:
            # Fallback to the memory-only generated icon
            try:
                icon_data = generate_html_icon()
                self.icon_img = tk.PhotoImage(data=icon_data)
                self.root.iconphoto(True, self.icon_img)
            except Exception:
                pass

        # --- UI SETUP ---
        header_frame = tk.Frame(root, bg="#1e1e1e")
        header_frame.pack(fill="x", pady=15)

        tk.Label(
            header_frame, 
            text="Launch Project:", 
            font=("Segoe UI", 12, "bold"), 
            fg="white", 
            bg="#1e1e1e"
        ).pack(side="left", padx=15)

        tk.Button(
            header_frame, 
            text="📁 Open Folder", 
            command=self.open_explorer,
            bg="#2d2d2d",
            fg="white",
            relief="flat",
            activebackground="#454545",
            activeforeground="white"
        ).pack(side="right", padx=15)

        self.list_frame = tk.Frame(root, bg="#1e1e1e")
        self.list_frame.pack(fill="both", expand=True, padx=15, pady=5)

        self.refresh_buttons()

    def refresh_buttons(self):
        # Safely clear old widgets
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        # Ensure directory exists safely
        if not os.path.exists(PROJECTS_DIR):
            try:
                os.makedirs(PROJECTS_DIR)
            except PermissionError:
                tk.Label(self.list_frame, text="Permission Denied.", fg="red", bg="#1e1e1e").pack()
                return

        # Scan folder using modern context manager
        with os.scandir(PROJECTS_DIR) as entries:
            for entry in entries:
                if entry.is_dir():
                    index_path = os.path.join(entry.path, "index.html")
                    if os.path.exists(index_path):
                        btn = tk.Button(
                            self.list_frame,
                            text=f"▶  {entry.name}",
                            command=lambda p=index_path: self.launch(p),
                            width=30,
                            anchor="w",
                            padx=15,
                            pady=8,
                            bg="#282828",
                            fg="#e44d26",
                            font=("Segoe UI", 10, "bold"),
                            relief="flat",
                            activebackground="#e44d26",
                            activeforeground="white",
                            cursor="hand2"
                        )
                        btn.pack(pady=4, fill="x")

    def launch(self, path):
        # Force strict resolution to prevent directory traversal
        abs_path = os.path.abspath(path)
        webbrowser.open(f"file://{abs_path}")

    def open_explorer(self):
        # Native, safe OS calls to open the directory
        if sys.platform == "win32":
            os.startfile(PROJECTS_DIR)
        elif sys.platform == "darwin":
            subprocess.run(["open", PROJECTS_DIR], check=False)
        else:
            subprocess.run(["xdg-open", PROJECTS_DIR], check=False)

if __name__ == "__main__":
    root = tk.Tk()
    app = LauncherApp(root)
    root.mainloop()