import os
import sys
import socket
import tkinter as tk
from tkinter import messagebox
import webbrowser
import subprocess
from urllib.parse import urlparse

# --- CONFIGURATION ---
# Safely determine the base directory whether running as a script or an EXE
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PATHS_FILE = os.path.join(BASE_DIR, "paths.txt")
VERSION = "v1.12.0"
REM = 16 

# Global socket reference to keep the port lock alive while the app runs
_instance_lock_socket = None

def enforce_single_instance():
    """Prevents multiple instances of the app from running simultaneously."""
    global _instance_lock_socket
    _instance_lock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Bind to a specific, arbitrary localhost port to act as a system-wide lock
        _instance_lock_socket.bind(("127.0.0.1", 54321))
    except socket.error:
        # If the port is already in use, another instance is running.
        temp_root = tk.Tk()
        temp_root.withdraw()
        messagebox.showinfo("Already Running", "An instance of HWA-Launcher is already open.")
        temp_root.destroy()
        sys.exit(0)

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

def extract_site_name(url):
    """Extracts the domain and subdomain to explicitly show where it is hosted."""
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
        
    parsed = urlparse(url)
    domain = parsed.netloc or parsed.path
    
    if domain.startswith("www."):
        domain = domain[4:]
        
    parts = domain.split(".")
    
    # Set the first part to ALL CAPS and clean up dashes/underscores
    first_part = parts[0].replace("-", " ").replace("_", " ").upper()
    
    # If there's a domain/host after the dot, add it in standard letters (Title Case)
    if len(parts) >= 2:
        second_part = parts[1].capitalize()
        return f"{first_part} {second_part}"
        
    return first_part

class LauncherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HWA-Launcher")
        self.root.minsize(rem(28), rem(15)) 
        self.root.configure(bg="#1e1e1e")
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

        # --- FOOTER UI ---
        self.footer_frame = tk.Frame(root, bg="#141414")
        self.footer_frame.pack(side="bottom", fill="x")
        
        disclaimer_text = f"{VERSION} | Vibe Coded by Serge-EMR | Disclaimer: Provided as-is."
        tk.Label(
            self.footer_frame, text=disclaimer_text, 
            font=("Segoe UI", 8), fg="#666666", bg="#141414", pady=rem(0.3)
        ).pack()

        # --- SMART SCROLLABLE CANVAS SETUP ---
        self.list_container = tk.Frame(root, bg="#1e1e1e")
        self.list_container.pack(fill="both", expand=True, padx=rem(1), pady=rem(0.5))
        
        self.list_container.columnconfigure(0, weight=1)
        self.list_container.rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(self.list_container, bg="#1e1e1e", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.list_container, orient="vertical", command=self.canvas.yview)
        
        self.canvas.grid(row=0, column=0, sticky="nsew")
        
        self.scrollable_frame = tk.Frame(self.canvas, bg="#1e1e1e")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        self.root.bind_all("<MouseWheel>", self._on_mousewheel)  
        self.root.bind_all("<Button-4>", self._on_mousewheel)    
        self.root.bind_all("<Button-5>", self._on_mousewheel)    

        self.refresh_buttons()

    def toggle_topmost(self):
        self.is_topmost = not self.is_topmost
        self.root.attributes("-topmost", self.is_topmost)
        if self.is_topmost:
            self.topmost_btn.configure(fg="#4CAF50", bg="#3d3d3d") 
        else:
            self.topmost_btn.configure(fg="#888888", bg="#2d2d2d") 

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)
        self._check_scrollbar()

    def _check_scrollbar(self):
        self.root.update_idletasks()
        if self.scrollable_frame.winfo_reqheight() > self.canvas.winfo_height():
            self.scrollbar.grid(row=0, column=1, sticky="ns")
        else:
            self.scrollbar.grid_remove()
            self.canvas.yview_moveto(0) 

    def _on_mousewheel(self, event):
        self.root.update_idletasks()
        if self.scrollable_frame.winfo_reqheight() <= self.canvas.winfo_height():
            return 
            
        if event.delta: 
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        elif event.num == 4: 
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5: 
            self.canvas.yview_scroll(1, "units")

    def auto_adjust_window(self):
        self.root.update_idletasks()
        head_h = self.header_frame.winfo_reqheight()
        foot_h = self.footer_frame.winfo_reqheight()
        list_h = self.scrollable_frame.winfo_reqheight()
        
        target_h = head_h + foot_h + list_h + rem(1.5) 
        max_h = self.root.winfo_screenheight() - rem(6)
        final_h = min(target_h, max_h)
        
        min_w, min_h = self.root.minsize()
        final_h = max(final_h, min_h)
        
        current_w = self.root.winfo_width()
        if current_w < min_w:
            current_w = min_w
            
        self.root.geometry(f"{current_w}x{final_h}")
        self._check_scrollbar()

    def refresh_buttons(self):
        # Destroy old widgets entirely to guarantee zero memory leaks
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if not os.path.exists(PATHS_FILE):
            try:
                with open(PATHS_FILE, "w") as f:
                    f.write("# Add the absolute paths or web links below\n")
                    f.write("# Use a pipe | to add a custom label to your items.\n")
                    f.write("# Example Windows: C:\\Users\\Name\\Documents\\Project\\index.html | My App\n")
                    f.write("# Example Executable: C:\\Tools\\server.exe | Local Server\n")
                    f.write("# Example Web Link: https://github.com | Code Repository\n")
            except PermissionError:
                tk.Label(self.scrollable_frame, text="Permission Denied to create paths.txt", fg="red", bg="#1e1e1e").pack()
                return

        valid_paths = []
        with open(PATHS_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    # Process for custom label
                    parts = line.split("|", 1)
                    raw_path = parts[0].strip()
                    custom_label = parts[1].strip() if len(parts) > 1 else None
                    
                    is_web = raw_path.startswith(("http://", "https://", "www."))
                    
                    if not is_web:
                        ext = os.path.splitext(raw_path)[1].lower()
                        # Strict Filter: Only accept HTML, EXE, BAT
                        if ext not in [".html", ".exe", ".bat"]:
                            continue
                            
                    valid_paths.append((raw_path, custom_label))
                    
                    # Prevent memory abuse on massive text files
                    if len(valid_paths) >= 20:
                        break

        if not valid_paths:
            tk.Label(
                self.scrollable_frame, 
                text="No valid paths found.\nClick 'Help' for instructions.", 
                fg="#888888", bg="#1e1e1e", justify="center"
            ).pack(pady=rem(1.5))
            self.auto_adjust_window()
            return

        for index, (path, label) in enumerate(valid_paths):
            is_web = path.startswith(("http://", "https://", "www."))
            
            # Formatting Display Name and Colors
            if is_web:
                display_name = label if label else extract_site_name(path)
                btn_fg = "#42A5F5" # Readable Blue
            else:
                ext = os.path.splitext(path)[1].lower()
                
                if ext == ".html":
                    if label:
                        display_name = label
                    else:
                        folder_name = os.path.basename(os.path.dirname(path))
                        display_name = folder_name if folder_name else os.path.basename(path)
                    btn_fg = "#4CAF50" # Green
                
                elif ext in [".exe", ".bat"]:
                    display_name = label if label else os.path.basename(path)
                    btn_fg = "#EF5350" # Readable Red

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
                fg=btn_fg,
                font=("Segoe UI", 10, "bold"),
                relief="flat",
                activebackground="#3d3d3d",
                activeforeground="#ffffff",
                cursor="hand2"
            )
            btn.pack(pady=rem(0.2), fill="x")
            
        # Optimization: Window adjust called ONCE after loop finishes.
        self.auto_adjust_window()

    def launch(self, path):
        if path.startswith(("http://", "https://", "www.")):
            webbrowser.open(path)
            return

        abs_path = os.path.abspath(path)
        if os.path.exists(abs_path):
            ext = os.path.splitext(abs_path)[1].lower()
            
            if ext == ".html":
                webbrowser.open(f"file://{abs_path}")
            elif ext in [".exe", ".bat"]:
                # Execute securely by locking to the application's native directory context
                cwd = os.path.dirname(abs_path)
                try:
                    if sys.platform == "win32":
                        # os.startfile acts exactly like a user double-clicking the app in Windows
                        os.startfile(abs_path)
                    else:
                        subprocess.Popen([abs_path], cwd=cwd)
                except Exception as e:
                    messagebox.showerror("Execution Error", f"Failed to launch application:\n{e}")
        else:
            messagebox.showerror("Error", f"File or Link not found:\n{path}\n\nPlease check your paths.txt file.")

    def edit_paths_file(self):
        if not os.path.exists(PATHS_FILE):
             with open(PATHS_FILE, "w") as f:
                    f.write("# Add the absolute paths or web links below\n")

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

        # Explicitly define the width and height of the help window
        # Bumped height slightly to accommodate the new custom label & color texts
        help_w = rem(28)  
        help_h = rem(44)  

        help_text = tk.Text(
            help_win, bg="#1e1e1e", fg="#cccccc", font=("Segoe UI", 10), 
            wrap="word", relief="flat", padx=rem(1.5), pady=rem(1.5), cursor="arrow"
        )
        help_text.pack(fill="both", expand=True)

        help_text.tag_configure("bold", font=("Segoe UI", 10, "bold"), foreground="white")
        help_text.tag_configure("title", font=("Segoe UI", 12, "bold"), foreground="white")
        help_text.tag_configure("blue", font=("Segoe UI", 10, "bold"), foreground="#42A5F5")
        help_text.tag_configure("green", font=("Segoe UI", 10, "bold"), foreground="#4CAF50")
        help_text.tag_configure("red", font=("Segoe UI", 10, "bold"), foreground="#EF5350")

        # Injecting the exact text provided
        help_text.insert("end", "How to Use this HWA Launcher\n\n", "title")
        
        help_text.insert("end", "1. Click the ")
        help_text.insert("end", "'📝 Edit Paths'", "bold")
        help_text.insert("end", " button.\n")
        
        help_text.insert("end", "2. A text file (paths.txt) will open in your editor.\n")
        
        help_text.insert("end", "3. Paste the exact, full path to your file or web link on a new line.\n\n")
        
        help_text.insert("end", "4. Optionally add a custom label using a pipe | character.\n\n")
        
        help_text.insert("end", "   Example (Windows .html):\n", "bold")
        help_text.insert("end", "   C:\\Users\\Name\\MyProject\\index.html\n\n")
        
        help_text.insert("end", "   Example (App Executable):\n", "bold")
        help_text.insert("end", "   C:\\Tools\\server.exe | Local Server\n\n")
        
        help_text.insert("end", "   Example (Web Link):\n", "bold")
        help_text.insert("end", "   https://github.com | My Code Repo\n\n")
        
        help_text.insert("end", "5. Save the text file and close it.\n")
        
        help_text.insert("end", "6. Click ")
        help_text.insert("end", "'🔄 Refresh'", "bold")
        help_text.insert("end", " in the app to load your new buttons.\n")
        
        help_text.insert("end", "7. Click any ▶ button to launch.\n\n")
        
        # --- NEW COLOR GUIDE TEXT ---
        help_text.insert("end", "Color Guide:\n", "bold")
        help_text.insert("end", "• Web Links ", "bold")
        help_text.insert("end", "appear in ")
        help_text.insert("end", "Blue.\n", "blue")
        
        help_text.insert("end", "• Local .html Files ", "bold")
        help_text.insert("end", "appear in ")
        help_text.insert("end", "Green.\n", "green")
        
        help_text.insert("end", "• Executables (.exe/.bat) ", "bold")
        help_text.insert("end", "appear in ")
        help_text.insert("end", "Red.\n\n", "red")
        
        help_text.insert("end", "NOTE: ", "bold")
        help_text.insert("end", "This app accepts only .html, .exe, .bat, and web links. Max 20 projects at a time.\n\n")
        
        help_text.insert("end", "Vibe Coded by Serge-EMR | c. 2026")

        help_text.configure(state="disabled")

        # Force UI update to fetch accurate main window dimensions
        self.root.update_idletasks()
        
        # Use rootx/rooty for accurate screen coordinates
        app_x = self.root.winfo_rootx()
        app_y = self.root.winfo_rooty()
        app_w = self.root.winfo_width()
        app_h = self.root.winfo_height()
        
        # Calculate strict center offsets using our hardcoded Help window sizes
        center_x = app_x + (app_w // 2) - (help_w // 2)
        center_y = app_y + (app_h // 2) - (help_h // 2)
        
        # Apply strict geometry to lock size and center position simultaneously
        help_win.geometry(f"{help_w}x{help_h}+{center_x}+{center_y}")

if __name__ == "__main__":
    # Check for another running instance before booting Tkinter
    enforce_single_instance()
    
    root = tk.Tk()
    app = LauncherApp(root)
    root.mainloop()