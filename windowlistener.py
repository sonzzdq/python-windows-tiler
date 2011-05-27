import win32gui
import time

from win32con import GW_OWNER
from win32con import GWL_STYLE
from win32con import WS_VISIBLE
from win32con import WS_EX_TOOLWINDOW
from win32con import WS_EX_CONTROLPARENT
from win32con import SW_SHOWNORMAL

class WindowListener:

    def __init__(self, floatList):

        self.floatList = floatList
        self.stop = False

    def callback (self, window, resultList):
        "Callback function for EnumWindows"

        if win32gui.IsWindowVisible(window):

            if not win32gui.GetWindow(window, GW_OWNER):

                value = win32gui.GetWindowLong(window, GWL_STYLE)

                if value & WS_VISIBLE:

                    if not value & WS_EX_TOOLWINDOW:

                        if value & WS_EX_CONTROLPARENT:

                            if win32gui.GetWindowPlacement(window)[1] == SW_SHOWNORMAL:

                                resultList.append(window)
                                return True

    def listen_to_windows(self, event):
        "Listens to windows, when the amount of windows changes it calls the event, passing the current windows"

        windows = []
        currentWindows = []
        self.oldAmount = 0

        print ("start loop")

        while not self.stop:

            time.sleep(0.1)

            windows = []
            reTile = False

            win32gui.EnumWindows(self.callback, windows)

            if len(windows) > self.oldAmount:

                for window in windows:

                    if window not in currentWindows:

                        if win32gui.GetClassName(window) not in self.floatList:

                            currentWindows.append(window)
                            reTile = True
                            print ("Add handle: ", window, win32gui.GetClassName(window))

            elif self.oldAmount > len(windows):

                for window in (oldTiledWindows - set(windows)):

                    if window in currentWindows:

                        currentWindows.remove(window)
                        reTile = True
                        print ("Remove handle: ", window)

            if reTile:

                event(currentWindows)
                self.oldAmount = len(windows)
                oldTiledWindows = set(currentWindows)

