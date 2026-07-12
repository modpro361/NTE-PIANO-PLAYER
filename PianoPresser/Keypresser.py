'''This code was made by modpro for the purpose of pressing keys on the the piano in nte automatically. Please use this code responsibly and ensure that it complies with any relevant terms of service or usage policies.'''
import os
import ctypes
from win32 import win32gui
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
  
def get_game_window():
    global game_hwnd
    # This searches for any window that contains your target text
    def enum_windows_callback(hwnd, extra):
        global game_hwnd
        window_title = win32gui.GetWindowText(hwnd)
        if "NTE" in window_title:  # Gets the nte window
            game_hwnd = hwnd
            return False  # Stops searching once found
        return True
    
    win32gui.EnumWindows(enum_windows_callback, None)
    
    if game_hwnd:
        # 1. If the window is minimized, restore it
        win32gui.ShowWindow(game_hwnd, 9) # 9 = SW_RESTORE
        
        # 2. Trick Windows into allowing a foreground change by tapping the ALT key
        # (Windows always allows foreground switches if the ALT key is interacting with the system)
        import win32com.client
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%') # Sends the ALT key
        
        # 3. Now bring it to the front
        win32gui.SetForegroundWindow(game_hwnd)
        print(f"Found game window! Handle: {game_hwnd}")
  
# Character map
char_map = {
    'q': 0x10, 'w': 0x11, 'e': 0x12, 'r': 0x13, 't': 0x14, 'z': 0x15, 'u': 0x16, 'i': 0x17, 'o': 0x18, 'p':0x19,
    'a': 0x1E, 's': 0x1F, 'd': 0x20, 'f': 0x21, 'g': 0x22, 'h': 0x23, 'j': 0x24, 'k': 0x25, 'l': 0x26,
    'y': 0x2C, 'x': 0x2D, 'c': 0x2E, 'v': 0x2F, 'b': 0x30, 'n': 0x31, 'm': 0x32 }

# Sending the message using the character map
get_game_window()

press_key(char_map['q']);
time.sleep(1)
release_key(char_map['q']); # h


