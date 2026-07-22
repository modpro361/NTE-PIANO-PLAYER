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


print(bring_nte_to_front("Calculator"))


# Example Usage: Simulates pressing the letter 'A' (Keycode 0) after a short safety delay
if __name__ == "__main__":
    print("Starting in 3 seconds... Click inside your target text box or application.")
    time.sleep(3)
    
    print("Injecting keypress...")
    keypress(0)  # Presses 'A'
    print("Done.")
