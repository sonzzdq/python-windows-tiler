import win32api
import win32gui

from win32con import SW_FORCEMINIMIZE
from win32con import SW_MINIMIZE
from win32con import SW_SHOWNORMAL
from win32con import WM_CLOSE
from win32con import GWL_STYLE
from win32con import WS_CAPTION
from win32con import WS_SIZEBOX
from win32con import SWP_DRAWFRAME
from win32con import SWP_SHOWWINDOW
from win32con import MONITOR_DEFAULTTONEAREST

def tile(window, windowPosition):
    "Tiles a window with the given coordinates"

    try:

        windowPlacement = win32gui.GetWindowPlacement(window)
        win32gui.SetWindowPos(window
                ,None
                ,windowPosition[0]
                ,windowPosition[1]
                ,windowPosition[2]
                ,windowPosition[3]
                ,SWP_SHOWWINDOW)

    except win32gui.error:

        print("Error while placing window: ", window)

def undecorate(window):
    "Removes borders and decoration from window"

    style = win32gui.GetWindowLong(window, GWL_STYLE)

    style |= WS_CAPTION 

    style |= WS_SIZEBOX 

    win32gui.SetWindowLong(window, GWL_STYLE, style)

    #win32gui.SetWindowPos(window ,None ,0 ,0 ,0 ,0 ,0x0020)

def current_monitor():
    "Returns current monitor based on focused window"

    return int(win32api.MonitorFromWindow(win32gui.GetForegroundWindow(),MONITOR_DEFAULTTONEAREST))

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
    set_cursor_window(window)

def focused_window():
    "Grabs the current window"

    return win32gui.GetForegroundWindow()

def window_under_cursor():
    "Grabs the window under the cursor"

    return win32gui.WindowFromPoint(win32api.GetCursorPos())

def set_cursor_window(window):
    "Moves cursor to the given window"

    rect = win32gui.GetWindowRect(window)
    win32api.SetCursorPos(((rect[2] + rect[0]) // 2, (rect[3] + rect[1]) // 2))
