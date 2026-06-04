import os
import sys
import pystray
import pyautogui as gui
from PIL import Image

# Platform check
if os.name != 'nt':
    import tkinter.messagebox as msgbox
    msgbox.showerror("Uh Oh!",message="Unfortunately Anti-Caps currently only works on Windows.")
    sys.exit()

from ctypes import WinDLL, windll

windll.shell32.SetCurrentProcessExplicitAppUserModelID("Anti-Caps")

def toggle():
    global active
    active = not active
    if not active:
        icon.remove_notification()
        icon.notify("Paused Capslock blocking")
        icon.icon=Image.open(resource_path("paused.png"))
        icon.title="Anti-Caps (Paused)"
        icon.update_menu()
    else:
        icon.remove_notification()
        icon.icon = Image.open(resource_path("anti-caps.png"))
        icon.title="Anti-Caps"
        icon.update_menu()
        icon.notify("Resumed Capslock blocking")

def quit(*args):
    global active
    global running
    active = False
    running = False
    icon.stop()

# Source - https://stackoverflow.com/a/13790741
# Posted by max, modified by community. See post 'Timeline' for change history
# Retrieved 2026-06-03, License - CC BY-SA 3.0

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

active = True
running = True

icon = pystray.Icon(name="Anti-Caps",
                    title="Anti-Caps",
                    icon=Image.open(resource_path("anti-caps.png")),
                    menu=pystray.Menu(
                        pystray.MenuItem(
                            text="Pause",
                            action=toggle,
                            checked=lambda arg: not active,
                        ),
                        pystray.MenuItem(
                            text="Exit",
                            action=quit,
                        )
                    ),
                )

icon.run_detached()

user32 = WinDLL('user32')

while running:
    while active:
        if user32.GetKeyState(0x14) != 0:
            gui.press('capslock')
