import win32gui
import win32api

from pwt.window import Window

from win32con import GW_OWNER
from win32con import GWL_STYLE
from win32con import WS_VISIBLE
from win32con import WS_EX_APPWINDOW
from win32con import WS_EX_CONTROLPARENT
from win32con import SW_SHOWNORMAL

class WindowCaller(object):

    def __init__(self, floats):

        self.floats = floats
        self.windows = []

        win32gui.EnumWindows(self.callback, self.windows)

    def callback (self, hwnd, resultList):
        "Callback function for EnumWindows"

        #Go through numerous checks to see if the hwnd is in the taskbar
        if win32gui.IsWindowVisible(hwnd):

            if not win32gui.GetWindow(hwnd, GW_OWNER):

                value = win32gui.GetWindowLong(hwnd, GWL_STYLE)

                if value & WS_EX_APPWINDOW:

                    if value & WS_EX_CONTROLPARENT:

                        if win32gui.GetWindowPlacement(hwnd)[1] == SW_SHOWNORMAL:
            
                            if win32gui.GetClassName(hwnd) not in self.floats:

                                print(hwnd)
                                resultList.append(Window(hwnd, self.floats))
                                return True

    def windows_for_monitor(self, monitor):
        "Return windows for monitor"

        monitorWindows = [] 

        for window in self.windows:

            if win32api.MonitorFromWindow(window.hwnd) == monitor:

                window.undecorate()
                window.update()

                monitorWindows.append(window)
            
        return monitorWindows
