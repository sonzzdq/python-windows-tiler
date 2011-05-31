import win32api
import win32gui

from win32con import SW_FORCEMINIMIZE
from win32con import SW_MINIMIZE
from win32con import SW_SHOWNORMAL
from win32con import WM_CLOSE
from win32con import GWL_EXSTYLE
from win32con import WS_BORDER
from win32con import WS_DLGFRAME
from win32con import SWP_FRAMECHANGED

import win32con
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

def undecorate(window):
    "Removes borders and decoration from window"

    style = win32gui.GetWindowLong(window, GWL_EXSTYLE)
    win32gui.SetWindowLong (window, GWL_EXSTYLE, 0)

    win32gui.SetWindowPos(window
            ,None
            ,0
            ,0
            ,0
            ,0
            ,win32con.SWP_FRAMECHANGED)

def current_monitor():
    "Returns current monitor based on focused window"

    return win32api.MonitorFromWindow(win32gui.GetForegroundWindow(),win32con.MONITOR_DEFAULTTONEAREST)

def get_monitor_workrectangle(monitor):

    return win32api.GetMonitorInfo(monitor)["Work"]

def show(window):
    "Shows the given window"

    win32gui.ShowWindow(window, SW_SHOWNORMAL)

def minimize(window):
    "Minimizes the given window"

    win32gui.ShowWindow(window, SW_MINIMIZE)

def close(window):
    "Closes the given window"

    win32gui.SendMessage(window, WM_CLOSE, 0, 0)

def focus(window):
    "Puts focus on the given window"

    win32gui.SetForegroundWindow(window)

def focused_window():
    "Grabs the current window"

    return win32gui.GetForegroundWindow()

def set_cursor_window(window):
    "Moves cursor to the given window"

    rect = win32gui.GetWindowRect(window)
    win32api.SetCursorPos(((rect[2] + rect[0]) // 2, (rect[3] + rect[1]) // 2))
