import os
import sys
import tkinter as tk
from tkinter import messagebox
import webbrowser
import subprocess

# --- CONFIGURATION ---
# Safely determine the base directory whether running as a script or an EXE
if getattr(sys, 'frozen', False):
    # Running as a compiled PyInstaller executable
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # Running as a normal Python script
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PATHS_FILE = os.path.join(BASE_DIR, "paths.txt")
VERSION = "v1.4.0"

# Base multiplier to simulate relative sizing (REM)
REM = 16 

def rem(value):
    """Helper function to convert float 'rem' values to integer pixels."""
    return int(value * REM)

def generate_html_icon():
    """Procedurally generates a 32x32 pixel HTML/Web Launcher icon in PPM format."""
    ppm = ["P3\n32 32\n255\n"]
    for y in range(32):
        for x in range(32):
            if 2 <= y <= 29 and 2 <= x <= 29:
                if y <= 7: 
                    if 4 <= x <= 6 and 4 <= y <= 5: ppm.append("255 95 86 ")
                    elif 9 <= x <= 11 and 4 <= y <= 5: ppm.append("255 189 46 ")
                    elif 14 <= x <= 16 and 4 <= y <= 5: ppm.append("39 201 63 ")
                    else: ppm.append("45 45 45 ")
                else:
                    if 10 <= x <= 22 and abs(y - 18) <= (22 - x) * 0.8: ppm.append("228 77 38 ")
                    else: ppm.append("30 30 30 ")
            else:
                ppm.append("20 20 20 ")
        ppm.append("\n")
    return "".join(ppm)

class LauncherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HTML-Launcher")
        
        # Maintains a sensible minimum size
        self.root.minsize(rem(28), rem(15)) 
        self.root.configure(bg="#1e1e1e")

        # Track Always on Top state
        self.is_topmost = False

        # --- SET SAFE PROCEDURAL ICON ---
        icon_path = os.path.join(BASE_DIR, "app_icon.ico")
        if os.path.exists(icon_path):
            try: self.root.iconbitmap(icon_path)
            except Exception: pass
        else:
            try:
                self.icon_img = tk.PhotoImage(data=generate_html_icon())
                self.root.iconphoto(True, self.icon_img)
            except Exception: pass

        # --- HEADER UI ---
        self.header_frame = tk.Frame(root, bg="#1e1e1e")
        self.header_frame.pack(fill="x", pady=rem(1), padx=rem(1))

        tk.Label(
            self.header_frame, text="Projects:", 
            font=("Segoe UI", 12, "bold"), fg="white", bg="#1e1e1e"
        ).pack(side="left")

        controls_frame = tk.Frame(self.header_frame, bg="#1e1e1e")
        controls_frame.pack(side="right")

        # NEW: Discrete Always on Top Toggle
        self.topmost_btn = tk.Button(controls_frame, text="📌 Pin", command=self.toggle_topmost,
                  bg="#2d2d2d", fg="#888888", relief="flat", padx=rem(0.5),
                  activebackground="#454545", activeforeground="white")
        self.topmost_btn.pack(side="left", padx=rem(0.2))

        tk.Button(controls_frame, text="❓ Help", command=self.show_help,
                  bg="#2d2d2d", fg="white", relief="flat", padx=rem(0.5),
                  activebackground="#454545", activeforeground="white").pack(side="left", padx=rem(0.2))

        tk.Button(controls_frame, text="🔄 Refresh", command=self.refresh_buttons,
                  bg="#2d2d2d", fg="white", relief="flat", padx=rem(0.5),
                  activebackground="#454545", activeforeground="white").pack(side="left", padx=rem(0.2))

        tk.Button(controls_frame, text="📝 Edit Paths", command=self.edit_paths_file,
                  bg="#2d2d2d", fg="white", relief="flat", padx=rem(0.5),
                  activebackground="#454545", activeforeground="white").pack(side="left", padx=rem(0.2))

        # --- FOOTER UI (Packed FIRST to protect it from being pushed off-screen) ---
        self.footer_frame = tk.Frame(root, bg="#141414")
        self.footer_frame.pack(side="bottom", fill="x")
        
        disclaimer_text = f"{VERSION} | Vibe Coded by Serge-EMR | Disclaimer: Provided as-is."
        tk.Label(
            self.footer_frame, text=disclaimer_text, 
            font=("Segoe UI", 8), fg="#666666", bg="#141414", pady=rem(0.3)
        ).pack()

        # --- SMART SCROLLABLE CANVAS SETUP ---
        # Packed after the footer so it securely fills only the space in between
        self.list_container = tk.Frame(root, bg="#1e1e1e")
        self.list_container.pack(fill="both", expand=True, padx=rem(1), pady=rem(0.5))
        
        # Grid layout allows us to easily show/hide the scrollbar without breaking layout
        self.list_container.columnconfigure(0, weight=1)
        self.list_container.rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(self.list_container, bg="#1e1e1e", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.list_container, orient="vertical", command=self.canvas.yview)
        
        self.canvas.grid(row=0, column=0, sticky="nsew")
        # Scrollbar grid is intentionally omitted here; added dynamically in _check_scrollbar
        
        self.scrollable_frame = tk.Frame(self.canvas, bg="#1e1e1e")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Event Bindings for Auto-Adjustment
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        self.root.bind_all("<MouseWheel>", self._on_mousewheel)  # Windows
        self.root.bind_all("<Button-4>", self._on_mousewheel)    # Linux up
        self.root.bind_all("<Button-5>", self._on_mousewheel)    # Linux down

        # Initialize lists
        self.refresh_buttons()

    def toggle_topmost(self):
        """Toggles the app window to be always on top of other windows."""
        self.is_topmost = not self.is_topmost
        self.root.attributes("-topmost", self.is_topmost)
        
        # Visually update the button so the user knows it is active
        if self.is_topmost:
            self.topmost_btn.configure(fg="#4CAF50", bg="#3d3d3d") # Green text, slightly lighter background
        else:
            self.topmost_btn.configure(fg="#888888", bg="#2d2d2d") # Revert to default muted state

    def _on_canvas_configure(self, event):
        """Ensures frame stretches to canvas width and checks if scrollbar is needed during resize."""
        self.canvas.itemconfig(self.canvas_window, width=event.width)
        self._check_scrollbar()

    def _check_scrollbar(self):
        """Conditionally shows or hides the scrollbar based on content vs window height."""
        self.root.update_idletasks()
        if self.scrollable_frame.winfo_reqheight() > self.canvas.winfo_height():
            self.scrollbar.grid(row=0, column=1, sticky="ns")
        else:
            self.scrollbar.grid_remove()
            self.canvas.yview_moveto(0) # Reset scroll position if snapped back to fit

    def _on_mousewheel(self, event):
        """Cross-platform mouse scroll behavior. Only scrolls if necessary."""
        self.root.update_idletasks()
        # Abort scrolling if everything fits on screen
        if self.scrollable_frame.winfo_reqheight() <= self.canvas.winfo_height():
            return 
            
        if event.delta: # Windows / Mac
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        elif event.num == 4: # Linux Up
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5: # Linux Down
            self.canvas.yview_scroll(1, "units")

    def auto_adjust_window(self):
        """Calculates the exact height required for all elements and adjusts window to fit."""
        self.root.update_idletasks()
        
        head_h = self.header_frame.winfo_reqheight()
        foot_h = self.footer_frame.winfo_reqheight()
        list_h = self.scrollable_frame.winfo_reqheight()
        
        # Total height = Header + Footer + Buttons + Container Padding
        target_h = head_h + foot_h + list_h + rem(1.5) 
        
        max_h = self.root.winfo_screenheight() - rem(6)
        final_h = min(target_h, max_h)
        
        # Ensure it never drops below the defined minimum sizes
        min_w, min_h = self.root.minsize()
        final_h = max(final_h, min_h)
        
        current_w = self.root.winfo_width()
        if current_w < min_w:
            current_w = min_w
            
        self.root.geometry(f"{current_w}x{final_h}")
        self._check_scrollbar()

    def refresh_buttons(self):
        # Destroy old widgets entirely before rebuilding
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if not os.path.exists(PATHS_FILE):
            try:
                with open(PATHS_FILE, "w") as f:
                    f.write("# Add the absolute paths to your index.html files below\n")
                    f.write("# Example Windows: C:\\Users\\Name\\Documents\\Project\\index.html\n")
                    f.write("# Example Mac/Linux: /Users/Name/Documents/Project/index.html\n")
            except PermissionError:
                tk.Label(self.scrollable_frame, text="Permission Denied to create paths.txt", fg="red", bg="#1e1e1e").pack()
                return

        valid_paths = []
        with open(PATHS_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    valid_paths.append(line)

        valid_paths = valid_paths[:20]

        if not valid_paths:
            tk.Label(
                self.scrollable_frame, 
                text="No valid paths found.\nClick 'Help' for instructions.", 
                fg="#888888", bg="#1e1e1e", justify="center"
            ).pack(pady=rem(1.5))
            self.auto_adjust_window()
            return

        for index, path in enumerate(valid_paths):
            folder_name = os.path.basename(os.path.dirname(path))
            display_name = folder_name if folder_name else os.path.basename(path)

            btn = tk.Button(
                self.scrollable_frame,
                text=f"{index + 1}. ▶  {display_name}",
                command=lambda p=path: self.launch(p),
                width=45,           
                anchor="w",         
                justify="left",     
                padx=rem(1),
                pady=rem(0.5),
                bg="#282828",
                fg="#4CAF50",
                font=("Segoe UI", 10, "bold"),
                relief="flat",
                activebackground="#3d3d3d",
                activeforeground="#81C784",
                cursor="hand2"
            )
            btn.pack(pady=rem(0.2), fill="x")
            
        # Trigger window resize logic after generating all buttons
        self.auto_adjust_window()

    def launch(self, path):
        abs_path = os.path.abspath(path)
        if os.path.exists(abs_path):
            webbrowser.open(f"file://{abs_path}")
        else:
            messagebox.showerror("Error", f"File not found:\n{abs_path}\n\nPlease check your paths.txt file.")

    def edit_paths_file(self):
        if not os.path.exists(PATHS_FILE):
             with open(PATHS_FILE, "w") as f:
                    f.write("# Add the absolute paths to your index.html files below\n")

        if sys.platform == "win32":
            os.startfile(PATHS_FILE)
        elif sys.platform == "darwin":
            subprocess.run(["open", PATHS_FILE], check=False)
        else:
            subprocess.run(["xdg-open", PATHS_FILE], check=False)

    def show_help(self):
        help_win = tk.Toplevel(self.root)
        help_win.title("How to Use")
        help_win.configure(bg="#1e1e1e")
        help_win.transient(self.root)
        help_win.grab_set()

        instructions = (
            "How to Use this HTML Launcher App\n\n"
            "1. Click the '📝 Edit Paths' button.\n"
            "2. A text file (paths.txt) will open in your editor.\n"
            "3. Paste the exact, full path to your .html file on a new line.\n\n"
            "   Example (Windows):\n"
            "   C:\\Users\\Name\\Documents\\MyProject\\index.html\n\n"
            "   Example (Mac/Linux):\n"
            "   /Users/Name/Documents/MyProject/index.html\n\n"
            "4. Save the text file and close it.\n"
            "5. Click '🔄 Refresh' in the app to load your new buttons.\n"
            "6. Click any ▶ button to launch the project in your browser.\n\n"
            "NOTE: The app allows a maximum of 20 projects at a time.\n\n"
	    "Vibe Coded by Serge-EMR | c. 2026"
        )

        tk.Label(
            help_win, text=instructions, font=("Segoe UI", 10), 
            fg="#cccccc", bg="#1e1e1e", justify="left", anchor="nw",
            padx=rem(1.5), pady=rem(1.5)
        ).pack(fill="both", expand=True)

        help_win.update_idletasks()
        
        app_x = self.root.winfo_x()
        app_y = self.root.winfo_y()
        app_width = self.root.winfo_width()
        app_height = self.root.winfo_height()
        
        help_width = help_win.winfo_width()
        help_height = help_win.winfo_height()
        
        center_x = app_x + (app_width // 2) - (help_width // 2)
        center_y = app_y + (app_height // 2) - (help_height // 2)
        
        help_win.geometry(f"+{center_x}+{center_y}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LauncherApp(root)
    root.mainloop()