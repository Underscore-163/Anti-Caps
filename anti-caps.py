import os
import sys
import pystray
import pyautogui as gui
from PIL import Image
from ctypes import WinDLL

user32 = WinDLL('user32')
running = True

def toggle():
    global running
    running = not running


def quit(*args):
    global running
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



menu = pystray.Menu(
    pystray.MenuItem(
        text="Pause",
        action=toggle,
        checked=lambda arg: not running,
    ),
    pystray.MenuItem(
        text="Exit",
        action=quit,
    )
)

icon = pystray.Icon(name="Anti-Caps",
                    icon=Image.open(resource_path("anti-caps.png")),
                    menu=menu, )

icon.run_detached()
while True:
    while running:
        if user32.GetKeyState(0x14) != 0:
            gui.press('capslock')