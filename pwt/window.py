import win32api
import win32gui

#For dummy window
from win32con import HWND_MESSAGE

from win32con import GW_OWNER

from win32con import SW_HIDE
from win32con import SW_SHOWNORMAL
from win32con import WM_CLOSE
from win32con import GWL_STYLE
from win32con import WS_CAPTION
from win32con import WS_SIZEBOX

from win32con import SWP_SHOWWINDOW
from win32con import SWP_FRAMECHANGED
from win32con import SWP_NOMOVE
from win32con import SWP_NOSIZE
from win32con import SWP_NOZORDER

from win32con import WS_EX_APPWINDOW
from win32con import WS_EX_CONTROLPARENT

class Window(object):

    def __init__(self, hwnd, floats):

        self.hwnd = hwnd
        self.floats = floats

    def __eq__(self, other):

        return self.hwnd == other.hwnd

    def __hash__(self):

        return hash(self.hwnd)

    def should_tile(self):

        #Go through numerous checks to see if the window is in the taskbar
        if win32gui.IsWindowVisible(self.hwnd):

            if not win32gui.GetWindow(self.hwnd, GW_OWNER):

                value = win32gui.GetWindowLong(self.hwnd, GWL_STYLE)

                if value & WS_EX_APPWINDOW:

                    if value & WS_EX_CONTROLPARENT:

                        if self.hwnd not in self.floats:

                            return True
        return False

    def has_decorations(self):

        if win32gui.GetWindowLong(self.hwnd, GWL_STYLE) & WS_CAPTION:

            return True
        
        return False

    def position(self, windowPosition):
        "Tiles a window with the given coordinates"

        try:

            windowPlacement = win32gui.GetWindowPlacement(self.hwnd)
            win32gui.SetWindowPlacement(self.hwnd, (windowPlacement[0]
                , SW_SHOWNORMAL
                , windowPlacement[2]
                , windowPlacement[3]
                , windowPosition))

        except win32gui.error:

            print("Error while placing window: ", self.hwnd)

    def undecorate(self):
        "Removes borders and decoration from window"

        try:

            style = win32gui.GetWindowLong(self.hwnd, GWL_STYLE)

            style -= WS_CAPTION 

            win32gui.SetWindowLong(self.hwnd, GWL_STYLE, style)

        except win32gui.error:

            print("Error while undecorating window: ", self.hwnd)

    def decorate(self):
        "Add borders and decoration to window"

        try:

            style = win32gui.GetWindowLong(self.hwnd, GWL_STYLE)

            style += WS_CAPTION

            win32gui.SetWindowLong(self.hwnd, GWL_STYLE, style)

        except win32gui.error:

            print("Error while decorating window: ", self.hwnd)

    def show(self):
        "Shows the given window"

        win32gui.ShowWindow(self.hwnd, SW_SHOWNORMAL)

    def hide(self):
        "Hide the given window"

        win32gui.ShowWindow(self.hwnd, SW_HIDE)

    def close(self):
        "Closes the given window"

        win32gui.SendMessage(self.hwnd, WM_CLOSE, 0, 0)

    def focus(self):
        "Puts focus on the given window"

        win32gui.SetForegroundWindow(self.hwnd)
        self.set_cursor_window()

    def set_cursor_window(self):
        "Moves cursor to the given window"

        rect = win32gui.GetWindowRect(self.hwnd)
        win32api.SetCursorPos(((rect[2] + rect[0]) // 2, (rect[3] + rect[1]) // 2))

    def update(self):
        "Update the window"

        win32gui.SetWindowPos(self.hwnd, 0, 0, 0, 0, 0, SWP_FRAMECHANGED + SWP_NOMOVE + SWP_NOSIZE + SWP_NOZORDER)

    def classname(self):
        "Returns the window's classname"

        return win32gui.GetClassName(self.hwnd)

    @staticmethod
    def destroy(hwnd):
        "Destroys the window"

        win32gui.DestroyWindow(hwnd)
    
    @staticmethod
    def focused_window(floats):
        "Grabs the current window"

        return Window(win32gui.GetForegroundWindow(), floats)

    @staticmethod
    def window_under_cursor(floats):
        "Grabs the window under the cursor"

        return Window(win32gui.WindowFromPoint(win32api.GetCursorPos()), floats)
