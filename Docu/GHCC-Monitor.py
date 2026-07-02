import webview
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Update the window creation line to use this function
html_file = resource_path('GHCC-Monitor.html')
icon_file = resource_path('GHCC-Monitor.ico')

window = webview.create_window(
'GHCC-Monitor',  # This sets your Window Title
    url=html_file, 
    width=1920, 
    height=1080,
    resizable=True
)

webview.start()