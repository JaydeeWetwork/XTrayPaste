"""
XTrayPaste - a tiny Windows tray app. (Fast build, hold to repeat.)

Sits in the system tray with an X icon. Press Alt+X anywhere and the
X symbol (U+1D54F MATHEMATICAL DOUBLE-STRUCK CAPITAL X) is typed
straight into whatever input box is active. Hold Alt+X down and it
keeps typing, like holding any other key.

Fast path: the symbol is sent as keystrokes, not through the clipboard.
No clipboard round trip, no paste delay, and your clipboard is never
touched. The only pause anywhere is the repeat cadence while held.

Tray menu:
    Copy X to clipboard   - loads the symbol onto the clipboard
    Quit                  - exits the app

Run the script:  python XTrayPaste.py
Or build the compiled exe with build.bat (PyInstaller, one file).

Deps for the script: pip install pystray Pillow keyboard
"""

import ctypes
import threading
import time

import keyboard
import pystray
from PIL import Image, ImageDraw

X_SYMBOL = "\U0001D54F"  # the double-struck X used by the X logo
CF_UNICODETEXT = 13
REPEAT_SECONDS = 0.035  # while held: one symbol about every 35 ms

_repeat_active = False


def make_icon_image(size=64):
    """Draw a bold white X on a black square, like the X brand mark."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)
    pad = size // 5
    w = max(3, size // 8)
    draw.line([(pad, pad), (size - pad, size - pad)], fill=(255, 255, 255, 255), width=w)
    draw.line([(size - pad, pad), (pad, size - pad)], fill=(255, 255, 255, 255), width=w)
    return img


def _repeat_loop():
    global _repeat_active
    try:
        while keyboard.is_pressed("alt") and keyboard.is_pressed("x"):
            keyboard.write(X_SYMBOL)
            time.sleep(REPEAT_SECONDS)
    finally:
        _repeat_active = False


def on_hotkey():
    """First symbol lands instantly; the loop keeps going while held."""
    global _repeat_active
    if _repeat_active:
        return
    _repeat_active = True
    threading.Thread(target=_repeat_loop, daemon=True).start()


def set_clipboard_text(text):
    """Minimal clipboard setter through the Windows API, no extra deps."""
    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32
    data = (text + "\0").encode("utf-16-le")
    handle = kernel32.GlobalAlloc(0x0002, len(data))  # GMEM_MOVEABLE
    ptr = kernel32.GlobalLock(handle)
    ctypes.memmove(ptr, data, len(data))
    kernel32.GlobalUnlock(handle)
    user32.OpenClipboard(0)
    user32.EmptyClipboard()
    user32.SetClipboardData(CF_UNICODETEXT, handle)
    user32.CloseClipboard()


def copy_only(icon, item):
    set_clipboard_text(X_SYMBOL)


def quit_app(icon, item):
    keyboard.unhook_all()
    icon.stop()


def main():
    # suppress=True swallows the hotkey so the app underneath never sees
    # a stray Alt+X, and the first symbol lands with zero delay.
    keyboard.add_hotkey("alt+x", on_hotkey, suppress=True)

    menu = pystray.Menu(
        pystray.MenuItem("Copy X to clipboard", copy_only),
        pystray.MenuItem("Quit", quit_app),
    )
    icon = pystray.Icon(
        "XTrayPaste",
        make_icon_image(),
        "X Tray: Alt+X types the X symbol, hold to repeat",
        menu,
    )
    icon.run()


if __name__ == "__main__":
    main()
