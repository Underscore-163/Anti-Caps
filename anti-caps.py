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
                    icon=Image.open("anti-caps.png"),
                    menu=menu, )

icon.run_detached()
while True:
    while running:
        if user32.GetKeyState(0x14) != 0:
            gui.press('capslock')