import win32gui
import win32api

from win32con import GW_OWNER
from win32con import GWL_STYLE
from win32con import WS_VISIBLE
from win32con import WS_EX_APPWINDOW
from win32con import WS_EX_CONTROLPARENT
from win32con import SW_SHOWNORMAL

class WindowCaller(object):

    def __init__(self, floatList):

        self.floatList = floatList
        self.windows = []

        win32gui.EnumWindows(self.callback, self.windows)

    def callback (self, window, resultList):
        "Callback function for EnumWindows"

        #Go through numerous checks to see if the window is in the taskbar
        if win32gui.IsWindowVisible(window):

            if not win32gui.GetWindow(window, GW_OWNER):

                value = win32gui.GetWindowLong(window, GWL_STYLE)

                if value & WS_EX_APPWINDOW:

                    if value & WS_EX_CONTROLPARENT:

                        if win32gui.GetWindowPlacement(window)[1] == SW_SHOWNORMAL:
            
                            if window not in self.floatList:

                                resultList.append(window)
                                return True

    def windows_for_monitor(self, monitor):
        "Return windows for monitor"

        monitorWindows = [] 

        for window in self.windows:

            if win32api.MonitorFromWindow(window) == monitor:

                monitorWindows.append(window)
            
        return monitorWindows
