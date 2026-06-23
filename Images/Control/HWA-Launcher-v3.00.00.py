import os
import sys
import socket
import tkinter as tk
from tkinter import messagebox
import webbrowser
import subprocess
from urllib.parse import urlparse
import ctypes

# --- CONFIGURATION ---
# Safely determine the base directory whether running as a script or an EXE
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PATHS_FILE = os.path.join(BASE_DIR, "paths.txt")
VERSION = "v3.00.00" # Version bumped to reflect hotfix
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
        temp_root.update()
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
    
    first_part = parts[0].replace("-", " ").replace("_", " ").upper()
    
    if len(parts) >= 2:
        second_part = parts[1].capitalize()
        return f"{first_part} {second_part}"
        
    return first_part

class LauncherApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"HWA-Launcher-{VERSION}")
        self.root.minsize(rem(21), rem(15)) 
        self.is_topmost = False
        
        # --- STATE ---
        self.is_dark_mode = True
        self.theme_colors = {}
        self.transparent_color = "#000001" 
        self.use_layered_hack = (sys.platform == "win32")

        # --- MENU BAR ---
        self.menubar = tk.Menu(self.root)
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label="📝 Edit Paths", command=self.edit_paths_file)
        self.file_menu.add_command(label="🔄 Refresh (F5)", command=self.refresh_buttons)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="❓ Help", command=self.show_help)
        self.menubar.add_cascade(label="Menu", menu=self.file_menu)
        self.root.config(menu=self.menubar)

        # --- KEY BINDINGS ---
        self.root.bind("<F5>", self.refresh_buttons)

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

        # --- HEADER UI (LEVEL 1) ---
        self.header_frame = tk.Frame(root)
        self.header_frame.pack(fill="x", pady=(rem(1), rem(0.2)), padx=rem(1))

        self.proj_label = tk.Label(self.header_frame, text="Item/s:", font=("Segoe UI", 12, "bold"))
        self.proj_label.pack(side="left")

        self.controls_frame = tk.Frame(self.header_frame)
        self.controls_frame.pack(side="right")

        self.topmost_btn = tk.Button(self.controls_frame, text="📌 Pin", command=self.toggle_topmost, relief="flat", padx=rem(0.5))
        self.topmost_btn.pack(side="left", padx=rem(0.2))

        self.theme_btn = tk.Button(self.controls_frame, text="☀️ Light Mode", command=self.toggle_theme, relief="flat", padx=rem(0.5))
        self.theme_btn.pack(side="left", padx=rem(0.2))

        # --- SUBHEADER UI (LEVEL 2 - OPACITY) ---
        self.subheader_frame = tk.Frame(root)
        self.subheader_frame.pack(fill="x", padx=rem(1), pady=(0, rem(0.5)))
        
        self.opacity_wrap = tk.Frame(self.subheader_frame)
        self.opacity_wrap.pack(side="right", fill="x", expand=False)
        
        lbl_text = "List Opacity:" if self.use_layered_hack else "App Opacity:"
        self.opacity_lbl = tk.Label(self.opacity_wrap, text=lbl_text, font=("Segoe UI", 9, "bold"))
        self.opacity_lbl.pack(side="left")

        self.opacity_scale = tk.Scale(self.opacity_wrap, from_=0.2, to=1.0, resolution=0.05, 
                                      orient="horizontal", showvalue=False, command=self.update_opacity, 
                                      bd=0, length=rem(8))
        self.opacity_scale.set(1.0)
        self.opacity_scale.pack(side="left", padx=(rem(0.5), 0))

        # --- BOTTOM RESIZE BUFFER ---
        # Critical Fix: This spacer prevents the transparent layered window from overlapping 
        # the OS's invisible resize grip at the bottom edge.
        self.bottom_buffer = tk.Frame(root, height=rem(0.8))
        self.bottom_buffer.pack_propagate(False)
        self.bottom_buffer.pack(side="bottom", fill="x")

        # --- LAYERED WINDOW HACK FOR ISOLATED TRANSPARENCY ---
        self.hole_frame = tk.Frame(root, bg=self.transparent_color, bd=0, highlightthickness=0)
        self.hole_frame.pack(fill="both", expand=True, padx=rem(1), pady=(0, rem(0.2)))

        if self.use_layered_hack:
            self.root.wm_attributes("-transparentcolor", self.transparent_color)
            
            self.list_window = tk.Toplevel(self.root) 
            
            # --- CRITICAL FIX: The "No-Withdraw" Hack ---
            self.list_window.geometry("1x1+-15000+-15000")
            self.list_window.attributes("-alpha", 0.0)
            
            self.list_window.overrideredirect(True)
            self.list_window.transient(self.root)
            self._remove_from_alt_tab(self.list_window)
            
            self.list_container = tk.Frame(self.list_window, bd=0, highlightthickness=0)
            self.list_container.pack(fill="both", expand=True)
            
            self.root.bind("<Configure>", self.sync_windows)
            self.hole_frame.bind("<Configure>", self.sync_windows)
            
            self.root.bind("<Map>", self._on_root_map)
            self.root.bind("<Unmap>", self._on_root_unmap)
            self.root.bind("<FocusIn>", self._on_root_focus)
        else:
            self.list_window = self.root
            self.list_container = tk.Frame(self.hole_frame, bd=0, highlightthickness=0)
            self.list_container.pack(fill="both", expand=True)

        # --- SMART SCROLLABLE CANVAS SETUP ---
        self.list_container.columnconfigure(0, weight=1)
        self.list_container.rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(self.list_container, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.list_container, orient="vertical", command=self.canvas.yview)
        
        self.canvas.grid(row=0, column=0, sticky="nsew")
        
        self.scrollable_frame = tk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        self.root.bind_all("<MouseWheel>", self._on_mousewheel)  
        self.root.bind_all("<Button-4>", self._on_mousewheel)    
        self.root.bind_all("<Button-5>", self._on_mousewheel)    

        self.apply_theme(resize=True)

        if sys.platform == "win32":
            self._disable_maximize_and_snap()

    def _disable_maximize_and_snap(self):
        """Disables the maximize button and Windows Aero Snap while keeping the window resizable."""
        try:
            self.root.update_idletasks()
            hwnd = int(self.root.wm_frame(), 16)
            GWL_STYLE = -16
            WS_MAXIMIZEBOX = 0x00010000
            
            style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_STYLE)
            ctypes.windll.user32.SetWindowLongW(hwnd, GWL_STYLE, style & ~WS_MAXIMIZEBOX)
        except Exception:
            pass

    def _remove_from_alt_tab(self, window):
        """Forces Windows to hide this specific window from Alt+Tab and Taskbar permanently."""
        if sys.platform != "win32": return
        try:
            window.update_idletasks()
            hwnd = int(window.wm_frame(), 16)
            GWL_EXSTYLE = -20
            WS_EX_TOOLWINDOW = 0x00000080
            WS_EX_APPWINDOW = 0x00040000
            
            style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            style = (style | WS_EX_TOOLWINDOW) & ~WS_EX_APPWINDOW
            ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
        except Exception:
            pass

    # --- Z-ORDER FIXES ---
    def _on_root_map(self, event):
        if event.widget is self.root and self.use_layered_hack:
            # Restore Opacity and let sync_windows snap it back to reality
            self.list_window.attributes("-alpha", float(self.opacity_scale.get()))
            self._remove_from_alt_tab(self.list_window) # Re-enforce just in case
            self.list_window.lift()
            self.sync_windows()

    def _on_root_unmap(self, event):
        if event.widget is self.root and self.use_layered_hack:
            # Banish off-screen and make invisible instead of withdrawing
            self.list_window.attributes("-alpha", 0.0)
            self.list_window.geometry("1x1+-15000+-15000")

    def _on_root_focus(self, event):
        if self.use_layered_hack:
            self.list_window.lift()

    def sync_windows(self, event=None):
        if not self.use_layered_hack: return
        if not self.root.winfo_viewable(): return
        
        if event and event.widget not in (self.root, self.hole_frame):
            return

        x = self.hole_frame.winfo_rootx()
        y = self.hole_frame.winfo_rooty()
        w = self.hole_frame.winfo_width()
        h = self.hole_frame.winfo_height()
        
        if w > 1 and h > 1:
            self.list_window.geometry(f"{w}x{h}+{x}+{y}")

    def update_opacity(self, value):
        val = float(value)
        if self.use_layered_hack:
            self.list_window.attributes("-alpha", val)
        else:
            self.root.attributes("-alpha", val)

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.apply_theme(resize=False)

    def apply_theme(self, resize=True):
        if self.is_dark_mode:
            self.theme_colors = {
                "bg_main": "#1e1e1e", "bg_list": "#1e1e1e",
                "fg_main": "white", "fg_mut": "#888888",
                "bg_btn": "#2d2d2d", "bg_btn_act": "#454545", "fg_btn": "white",
                "item_bg": "#282828",
                "item_fg_web": "#42A5F5", "item_fg_html": "#4CAF50", "item_fg_exe": "#EF5350",
                "slider_trough": "#454545"
            }
            self.theme_btn.config(text="☀️ Light Mode")
        else:
            self.theme_colors = {
                "bg_main": "#f0f0f0", "bg_list": "#ffffff",
                "fg_main": "black", "fg_mut": "#555555",
                "bg_btn": "#dddddd", "bg_btn_act": "#cccccc", "fg_btn": "black",
                "item_bg": "#f9f9f9",
                "item_fg_web": "#1565C0", "item_fg_html": "#2E7D32", "item_fg_exe": "#C62828",
                "slider_trough": "#cccccc"
            }
            self.theme_btn.config(text="🌙 Dark Mode")

        tc = self.theme_colors

        # Style Menus 
        self.file_menu.configure(bg=tc["bg_list"], fg=tc["fg_main"], activebackground=tc["bg_btn_act"], activeforeground=tc["fg_btn"])

        self.root.configure(bg=tc["bg_main"])
        self.header_frame.configure(bg=tc["bg_main"])
        self.proj_label.configure(bg=tc["bg_main"], fg=tc["fg_main"])
        self.controls_frame.configure(bg=tc["bg_main"])
        self.subheader_frame.configure(bg=tc["bg_main"])
        self.opacity_wrap.configure(bg=tc["bg_main"])
        self.opacity_lbl.configure(bg=tc["bg_main"], fg=tc["fg_main"])
        
        # Style the new buffer frame
        self.bottom_buffer.configure(bg=tc["bg_main"])

        btn_fg_pin = "#4CAF50" if self.is_topmost else tc["fg_mut"]
        self.topmost_btn.configure(bg=tc["bg_btn"], fg=btn_fg_pin, activebackground=tc["bg_btn_act"], activeforeground=tc["fg_btn"])
        self.theme_btn.configure(bg=tc["bg_btn"], fg=tc["fg_main"], activebackground=tc["bg_btn_act"], activeforeground=tc["fg_btn"])
        
        self.opacity_scale.configure(bg=tc["bg_main"], fg=tc["fg_main"], troughcolor=tc["slider_trough"], activebackground=tc["bg_btn_act"])

        self.list_container.configure(bg=tc["bg_list"])
        self.canvas.configure(bg=tc["bg_list"])
        self.scrollable_frame.configure(bg=tc["bg_list"])

        self.refresh_buttons(resize=resize)

    def toggle_topmost(self):
        self.is_topmost = not self.is_topmost
        self.root.attributes("-topmost", self.is_topmost)
        
        if self.use_layered_hack:
            self.list_window.attributes("-topmost", self.is_topmost)
            
        btn_fg_pin = "#4CAF50" if self.is_topmost else self.theme_colors["fg_mut"]
        self.topmost_btn.configure(fg=btn_fg_pin) 

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
        sub_h = self.subheader_frame.winfo_reqheight()
        list_h = self.scrollable_frame.winfo_reqheight()
        buf_h = self.bottom_buffer.winfo_reqheight()
        
        target_h = head_h + sub_h + list_h + buf_h + rem(2.5) 
        max_h = self.root.winfo_screenheight() - rem(6)
        final_h = min(target_h, max_h)
        
        min_w, min_h = self.root.minsize()
        final_h = max(final_h, min_h)
        
        current_w = self.root.winfo_width()
        if current_w < min_w:
            current_w = min_w
            
        self.root.geometry(f"{current_w}x{final_h}")
        self._check_scrollbar()
        
        if self.use_layered_hack:
            self.sync_windows()

    def refresh_buttons(self, event=None, resize=True):
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
                tk.Label(self.scrollable_frame, text="Permission Denied to create paths.txt", fg="red", bg=self.theme_colors["bg_list"]).pack()
                return

        valid_paths = []
        with open(PATHS_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    parts = line.split("|", 1)
                    raw_path = parts[0].strip()
                    custom_label = parts[1].strip() if len(parts) > 1 else None
                    
                    is_web = raw_path.startswith(("http://", "https://", "www."))
                    
                    if not is_web:
                        ext = os.path.splitext(raw_path)[1].lower()
                        if ext not in [".html", ".exe", ".bat"]:
                            continue
                            
                    valid_paths.append((raw_path, custom_label))
                    
                    if len(valid_paths) >= 20:
                        break

        if not valid_paths:
            tk.Label(
                self.scrollable_frame, 
                text="No valid paths found.\nClick 'Help' in the menu.", 
                fg=self.theme_colors["fg_mut"], bg=self.theme_colors["bg_list"], justify="center"
            ).pack(pady=rem(1.5))
            
            if resize:
                self.auto_adjust_window()
            else:
                self._check_scrollbar()
            return

        for index, (path, label) in enumerate(valid_paths):
            is_web = path.startswith(("http://", "https://", "www."))
            
            if is_web:
                display_name = label if label else extract_site_name(path)
                btn_fg = self.theme_colors["item_fg_web"]
            else:
                ext = os.path.splitext(path)[1].lower()
                if ext == ".html":
                    if label:
                        display_name = label
                    else:
                        folder_name = os.path.basename(os.path.dirname(path))
                        display_name = folder_name if folder_name else os.path.basename(path)
                    btn_fg = self.theme_colors["item_fg_html"]
                elif ext in [".exe", ".bat"]:
                    display_name = label if label else os.path.basename(path)
                    btn_fg = self.theme_colors["item_fg_exe"]

            btn = tk.Button(
                self.scrollable_frame,
                text=f"{index + 1}. ▶  {display_name}",
                command=lambda p=path: self.launch(p),
                width=34,            
                anchor="w",          
                justify="left",      
                padx=rem(0.5),
                pady=rem(0.1), 
                bg=self.theme_colors["item_bg"],
                fg=btn_fg,
                font=("Segoe UI", 10, "bold"),
                relief="flat",
                activebackground=self.theme_colors["bg_btn_act"],
                activeforeground=self.theme_colors["fg_main"],
                cursor="hand2"
            )
            btn.pack(pady=rem(0.05), fill="x")
            
        if resize:
            self.auto_adjust_window()
        else:
            self._check_scrollbar()

    def launch(self, path):
        if path.startswith(("http://", "https://")):
            webbrowser.open(path)
            return
        elif path.startswith("www."):
            webbrowser.open("http://" + path)
            return
        elif path.startswith(("javascript:", "data:", "file:")):
            messagebox.showerror("Security Block", "Potentially unsafe web protocol blocked.")
            return

        abs_path = os.path.abspath(path)
        if os.path.exists(abs_path):
            ext = os.path.splitext(abs_path)[1].lower()
            
            if ext == ".html":
                webbrowser.open(f"file://{abs_path}")
            elif ext in [".exe", ".bat"]:
                cwd = os.path.dirname(abs_path)
                try:
                    if sys.platform == "win32":
                        os.startfile(abs_path)
                    else:
                        subprocess.Popen([abs_path], cwd=cwd)
                except Exception as e:
                    messagebox.showerror("Execution Error", f"Failed to launch application:\n{e}")
            else:
                messagebox.showerror("Security Block", "Only .html, .exe, and .bat files are allowed.")
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
        help_win.configure(bg=self.theme_colors["bg_main"])
        help_win.transient(self.root)
        help_win.grab_set()

        help_w = rem(25)  
        help_h = rem(40)  

        help_text = tk.Text(
            help_win, bg=self.theme_colors["bg_list"], fg=self.theme_colors["fg_main"], font=("Segoe UI", 10), 
            wrap="word", relief="flat", padx=rem(1.5), pady=rem(1.5), cursor="arrow"
        )
        help_text.pack(fill="both", expand=True)

        help_text.tag_configure("bold", font=("Segoe UI", 10, "bold"), foreground=self.theme_colors["fg_main"])
        help_text.tag_configure("title", font=("Segoe UI", 12, "bold"), foreground=self.theme_colors["fg_main"])
        help_text.tag_configure("blue", font=("Segoe UI", 10, "bold"), foreground=self.theme_colors["item_fg_web"])
        help_text.tag_configure("green", font=("Segoe UI", 10, "bold"), foreground=self.theme_colors["item_fg_html"])
        help_text.tag_configure("red", font=("Segoe UI", 10, "bold"), foreground=self.theme_colors["item_fg_exe"])

        help_text.insert("end", "How to Use this HWA Launcher Tool\n\n", "title")
        help_text.insert("end", "1. Open the Menu and click ")
        help_text.insert("end", "'📝 Edit Paths'", "bold")
        help_text.insert("end", ".\n")
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
        help_text.insert("end", "6. Press ")
        help_text.insert("end", "F5", "bold")
        help_text.insert("end", " or click Menu -> Refresh to load your new buttons.\n")
        help_text.insert("end", "7. Click any ▶ button to launch.\n\n")
        
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
        help_text.insert("end", "This app accepts only .html, .exe, .bat, and web links. Max 20 items at a time.\n\n")
        help_text.insert("end", f"--- DISCLAIMER ---\n", "bold")
        help_text.insert("end", f"Provided as-is.\n{VERSION} | Vibe Coded by Serge-EMR | c. 2026")

        help_text.configure(state="disabled")

        self.root.update_idletasks()
        
        app_x = self.root.winfo_rootx()
        app_y = self.root.winfo_rooty()
        app_w = self.root.winfo_width()
        app_h = self.root.winfo_height()
        
        center_x = app_x + (app_w // 2) - (help_w // 2)
        center_y = app_y + (app_h // 2) - (help_h // 2)
        
        help_win.geometry(f"{help_w}x{help_h}+{center_x}+{center_y}")

if __name__ == "__main__":
    enforce_single_instance()
    
    root = tk.Tk()
    app = LauncherApp(root)
    root.mainloop()