import win32api
import win32gui

from win32con import SW_FORCEMINIMIZE
from win32con import WM_CLOSE

def tile(window, rectangleCoordinates):
    "Tiles a window with the given coordinates"

    try:

        windowPlacement = win32gui.GetWindowPlacement(window)
        win32gui.SetWindowPlacement(window, (windowPlacement[0]
            , windowPlacement[1]
            , windowPlacement[2]
            , windowPlacement[3]
            , rectangleCoordinates))
    except win32gui.error:

        print("Error while placing window: ", window)

def minimize(window):
    "Minimizes the given window"

    win32gui.ShowWindow(window, SW_FORCEMINIMIZE)

def close(window):
    "Closes the given window"

    win32gui.SendMessage(window, WM_CLOSE, 0, 0)

def focus(window):
    "Puts focus on the given window"

    win32gui.SetForegroundWindow(window)

def get_focused_window():
    "Grabs the current window"

    return win32gui.GetForegroundWindow()

def set_cursor_window(window):
    "Moves cursor to the given window"

    rect = win32gui.GetWindowRect(window)
    win32api.SetCursorPos(((rect[2] + rect[0]) // 2, (rect[3] + rect[1]) // 2))
