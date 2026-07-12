import os
import ctypes
from win32 import win32gui
import win32process
import win32api
import win32con
from window_helper import WindowMgr
import time

# Global variable to hold the window handle
game_hwnd = 0

PUL = ctypes.POINTER(ctypes.c_ulong)

class KeyBdInput(ctypes.Structure):
   _fields_ = [("wVk", ctypes.c_ushort),
               ("wScan", ctypes.c_ushort),
               ("dwFlags", ctypes.c_ulong),
               ("time", ctypes.c_ulong),
               ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
   _fields_ = [("uMsg", ctypes.c_ulong),
               ("wParamL", ctypes.c_short),
               ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
   _fields_ = [("dx", ctypes.c_long),
               ("dy", ctypes.c_long),
               ("mouseData", ctypes.c_ulong),
               ("dwFlags", ctypes.c_ulong),
               ("time", ctypes.c_ulong),
               ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
   _fields_ = [("ki", KeyBdInput),
               ("mi", MouseInput),
               ("hi", HardwareInput)]


class Input(ctypes.Structure):
   _fields_ = [("type", ctypes.c_ulong),
               ("ii", Input_I)]


def press_key(key):
   extra = ctypes.c_ulong(0)
   ii_ = Input_I()

   flags = 0x0008

   ii_.ki = KeyBdInput(0, key, flags, 0, ctypes.pointer(extra))
   x = Input(ctypes.c_ulong(1), ii_)
   ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def release_key(key):
   extra = ctypes.c_ulong(0)
   ii_ = Input_I()

   flags = 0x0008 | 0x0002

   ii_.ki = KeyBdInput(0, key, flags, 0, ctypes.pointer(extra))
   x = Input(ctypes.c_ulong(1), ii_)
   ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def force_foreground(hwnd):
    """Reliable foreground switch that bypasses Windows' foreground lock
    by temporarily attaching input threads."""
    fg_hwnd = win32gui.GetForegroundWindow()
    fg_thread = win32process.GetWindowThreadProcessId(fg_hwnd)[0]
    target_thread = win32process.GetWindowThreadProcessId(hwnd)[0]
    current_thread = win32api.GetCurrentThreadId()

    attached_fg = False
    attached_target = False

    try:
        if fg_thread != current_thread:
            win32process.AttachThreadInput(current_thread, fg_thread, True)
            attached_fg = True
        if target_thread != current_thread:
            win32process.AttachThreadInput(current_thread, target_thread, True)
            attached_target = True

        win32gui.ShowWindow(hwnd, 9)  # SW_RESTORE
        win32gui.SetForegroundWindow(hwnd)
        win32gui.BringWindowToTop(hwnd)
    finally:
        if attached_fg:
            win32process.AttachThreadInput(current_thread, fg_thread, False)
        if attached_target:
            win32process.AttachThreadInput(current_thread, target_thread, False)


def get_game_window():
    global game_hwnd
    # This searches for any window that contains "NTE" in its title, but we want to be more specific to avoid false positives.
    def enum_windows_callback(hwnd, extra):
        global game_hwnd
        window_title = win32gui.GetWindowText(hwnd)
        class_name = win32gui.GetClassName(hwnd)
        # Match the real game window specifically: exact title "NTE"
        # and the UnrealWindow class, to avoid matching VS Code or other windows that contains "NTE" as a substring
        if window_title.strip() == "NTE" and class_name == "UnrealWindow":
            game_hwnd = hwnd
            return False  # Stops searching once found
        return True

    win32gui.EnumWindows(enum_windows_callback, None)

    if game_hwnd:
        force_foreground(game_hwnd)
        time.sleep(0.3)  # give NTE time to actually process focus

        current_fg = win32gui.GetForegroundWindow()
        print(f"Found game window! Handle: {game_hwnd}")
        print(f"Foreground now: {win32gui.GetWindowText(current_fg)}")

        if current_fg != game_hwnd:
            print("WARNING: Foreground switch did not stick.")
    else:
        print("NTE window not found.")


# Character map
char_map = {
    'q': 0x10, 'w': 0x11, 'e': 0x12, 'r': 0x13, 't': 0x14, 'z': 0x15, 'u': 0x16, 'i': 0x17, 'o': 0x18, 'p': 0x19,
    'a': 0x1E, 's': 0x1F, 'd': 0x20, 'f': 0x21, 'g': 0x22, 'h': 0x23, 'j': 0x24, 'k': 0x25, 'l': 0x26,
    'y': 0x2C, 'x': 0x2D, 'c': 0x2E, 'v': 0x2F, 'b': 0x30, 'n': 0x31, 'm': 0x32}

# Debug, list every window with "NTE" in the title so we can confirm the correct one is being found
#def list_nte_windows(hwnd, extra):
#    #title = win32gui.GetWindowText(hwnd)
#    if "NTE" in title:
#        visible = win32gui.IsWindowVisible(hwnd)
#        class_name = win32gui.GetClassName(hwnd)
#        print(f"hwnd={hwnd}, title='{title}', visible={visible}, class='{class_name}'")

print("--- Windows matching 'NTE' ---")
win32gui.EnumWindows(list_nte_windows, None)
print("--- End list ---")

# Sending the message using the character map
get_game_window()

press_key(char_map['q'])
time.sleep(1)
release_key(char_map['q'])