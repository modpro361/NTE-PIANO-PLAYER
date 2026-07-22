'''This is a a piano player for the piano in nte, this program can read sheet music and play it on nte.'''
#Please this verson is made for mac
import time
from Quartz.CoreGraphics import (
    CGEventCreateKeyboardEvent,
    CGEventPost,
    kCGHIDEventTap
)
from AppKit import NSWorkspace, NSRunningApplication
from Cocoa import NSApplicationActivateIgnoringOtherApps

#Simulates a low-level keyboard press and release on macOS.
def keypress(key_code, hold_time=0.1):
    key_down = CGEventCreateKeyboardEvent(None, key_code, True)
    CGEventPost(kCGHIDEventTap, key_down)
    time.sleep(hold_time)
    key_up = CGEventCreateKeyboardEvent(None, key_code, False)
    CGEventPost(kCGHIDEventTap, key_up)


def bring_nte_to_front(app_name):
    # Get all running applications
    workspace = NSWorkspace.sharedWorkspace()
    running_apps = workspace.runningApplications()
    
    # Search for nte
    for app in running_apps:
        if app.localizedName() == app_name:
            app.activateWithOptions_(NSApplicationActivateIgnoringOtherApps)
            return f"Successfully brought '{app_name}' to the foreground."
            
    return f"Application '{app_name}' is not currently running."

# Character map
char_map = {
    'q': 0x10, 'w': 0x11, 'e': 0x12, 'r': 0x13, 't': 0x14, 'z': 0x2C, 'u': 0x16, 'i': 0x17, 'o': 0x18, 'p': 0x19,
    'a': 0x1E, 's': 0x1F, 'd': 0x20, 'f': 0x21, 'g': 0x22, 'h': 0x23, 'j': 0x24, 'k': 0x25, 'l': 0x26,
    'y': 0x15, 'x': 0x2D, 'c': 0x2E, 'v': 0x2F, 'b': 0x30, 'n': 0x31, 'm': 0x32, 'shift': 0x2A, 'ctrl': 0x1D }


# Example Usage: Simulates pressing the letter 'A' (Keycode 0) after a short safety delay
if __name__ == "__main__":
    print(bring_nte_to_front("Calculator"))
    time.sleep(3)
    
    print("Injecting keypress...")
    keypress(0)  # Presses 'A'
    print("Done.")
