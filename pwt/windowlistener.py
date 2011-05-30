import time
import win32gui

from win32con import GW_OWNER
from win32con import GWL_STYLE
from win32con import WS_VISIBLE
from win32con import WS_EX_APPWINDOW
from win32con import WS_EX_CONTROLPARENT
from win32con import SW_SHOWNORMAL

class WindowListener(object):

    def __init__(self, floatList):

        self.floatList = floatList
        self.stop = False
        self.oldAmount = 0
        self.currentWindows = []
        self.oldTiledwindows = []

    def callback (self, window, resultList):
        "Callback function for EnumWindows"

        #Go through numerous checks to see if the window is in the taskbar
        if win32gui.IsWindowVisible(window):

            if not win32gui.GetWindow(window, GW_OWNER):

                value = win32gui.GetWindowLong(window, GWL_STYLE)

                if value & WS_EX_APPWINDOW:

                    if value & WS_EX_CONTROLPARENT:

                        if win32gui.GetWindowPlacement(window)[1] == SW_SHOWNORMAL:

                            resultList.append(window)
                            return True

    def listen_to_windows(self, handler):
        "Enumerateswindows, when the amount of windows changes it calls the handler, passing the current windows"

        callHandler = False
        self.windows = []

        #enumerate all self.windows
        win32gui.EnumWindows(self.callback, self.windows)

        #check for window changement
        if len(self.windows) > self.oldAmount:

            for window in self.windows:

                if window not in self.currentWindows:

                    if win32gui.GetClassName(window) not in self.floatList:

                        self.currentWindows.append(window)
                        callHandler = True
                        print ("Add handle: ", window, win32gui.GetClassName(window))

        elif self.oldAmount > len(self.windows):

            for window in (self.oldTiledWindows - set(self.windows)):

                if window in self.currentWindows:

                    self.currentWindows.remove(window)
                    callHandler = True
                    print ("Remove handle: ", window)

        if callHandler:

            #call the handler
            handler(self.currentWindows)
            self.oldAmount = len(self.windows)
            self.oldTiledWindows = set(self.currentWindows)

    def reload_windows(self, currentWindows):

        self.currentWindows = currentWindows
        self.oldTiledWindows = set(currentWindows)
        self.oldAmount = len(self.currentWindows)
