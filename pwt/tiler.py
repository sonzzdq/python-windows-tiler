import ctypes
import pwt.windowutilities

from win32con import SPI_GETWORKAREA

import time
class Tiler(object):

    def __init__(self):

        class Crect(ctypes.Structure):
            _fields_ = [('left', ctypes.c_ulong),
                    ('top', ctypes.c_ulong),
                    ('right', ctypes.c_ulong),
                    ('bottom', ctypes.c_ulong)]

        r = Crect()

        ctypes.windll.user32.SystemParametersInfoA(SPI_GETWORKAREA, 0, ctypes.byref(r), 0)

        self.width = r.right - r.left
        self.height = r.bottom - r.top

        self.masterareaWidth = self.width // 2
        self.masterareaSize = 1

        self.windows = []

    def tile_windows(self, windows=None):
        "Tiles all windows, if windows are given it sets them to the self.windows attribute"

        if windows is not None:

            self.windows = windows

        if len(self.windows) > 1:

            if self.masterareaSize == len(self.windows):

                height = self.height

            else:

                height = self.height // (len(self.windows) - self.masterareaSize)

            if self.masterareaSize >= len(self.windows):

                heightMaster = self.height // len(self.windows)
                width = self.width

            else:

                heightMaster = self.height // self.masterareaSize
                width = self.masterareaWidth

            for i, window in enumerate(self.windows):

                if i in range(self.masterareaSize):

                    rectangleCoordinates = (0,i * heightMaster, width, (i + 1) * heightMaster)

                else:

                    rectangleCoordinates = (width, (i - self.masterareaSize) * height, self.width, (i - self.masterareaSize + 1) * height)

                pwt.windowutilities.tile(window, rectangleCoordinates)

        elif len(self.windows) > 0:

            pwt.windowutilities.tile(self.windows[0], (0, 0, self.width, self.height))

    ############################################
    ### Start of the commands
    ############################################

    def decrease_masterarea_width(self):
        "Decreases the masterarea width by 100px"

        if self.masterareaWidth >= 100:

            #decrease master areaWidth 
            self.masterareaWidth -= 100
            print("master area -= 100")

            self.tile_windows()

    def increase_masterarea_width(self):
        "Increases the masterarea width by 100px"

        if self.width - self.masterareaWidth >= 100:

            #increase master areaWidth 
            self.masterareaWidth += 100
            print("master area += 100")

            self.tile_windows()

    def set_focus_down(self):
        "Sets focus on the next window"

        #get focused window
        window = pwt.windowutilities.get_focused_window()

        #only grab and move the focus if it is in the self
        if window in self.windows:

            i = self.windows.index(window) + 1

            #if the index after the foreground's is out of range, assign 0
            if i >= len(self.windows):

                i = 0

            #focus window and cursor
            pwt.windowutilities.focus(self.windows[i])
            pwt.windowutilities.set_cursor_window(self.windows[i])

        else:

            self.set_focus_to_masterarea()

    def set_focus_up(self):
        "Sets focus on the previous window"

        #get focused window
        window = pwt.windowutilities.get_focused_window()

        #only grab and move the focus if it is in the self
        if window in self.windows:

            i = self.windows.index(window) - 1

            #if the index before the foreground's is out of range, assign last index
            if i < 0:

                i = len(self.windows) - 1

            #focus window and cursor
            pwt.windowutilities.focus(self.windows[i])
            pwt.windowutilities.set_cursor_window(self.windows[i])

        else:

            self.set_focus_to_masterarea()

    def set_focus_to_masterarea(self):
        "Sets focus on the masterarea"

        if len(self.windows):

            pwt.windowutilities.focus(self.windows[0])
            pwt.windowutilities.set_cursor_window(self.windows[0])

    def move_focusedwindow_down(self):
        "Switches the window to the next position"
        
        #get focused window
        window = pwt.windowutilities.get_focused_window()

        #only grab and move the window if it is in the self
        if window in self.windows:

            i = self.windows.index(pwt.windowutilities.get_focused_window())

            #if the foreground window is the last window, shift everything and place it first
            if i == len(self.windows) - 1:

                self.windows[0], self.windows[1:] = self.windows[i], self.windows[:i]

            #else shift it with the following window
            else:

                self.windows[i], self.windows[i + 1] = self.windows[i + 1], self.windows[i]

            print ("change order down")
            self.tile_windows()

    def move_focusedwindow_up(self):
        "Switches the window to the previous position"

        window = pwt.windowutilities.get_focused_window()

        #only grab and move the window if it is in the self
        if window in self.windows:

            i = self.windows.index(pwt.windowutilities.get_focused_window())

            #if the foreground window is first, shift everything and place it last
            if i == 0:

                j = len(self.windows) - 1
                self.windows[j], self.windows[:j] = self.windows[0], self.windows[1:]

            #else shift it with the trailing window
            else:

                j = i - 1
                self.windows[i], self.windows[j] = self.windows[j], self.windows[i]

            print ("change order up")
            self.tile_windows()

    def move_focusedwindow_to_masterarea(self):
        "Moves the focused window to the first place in the masterarea"

        window = pwt.windowutilities.get_focused_window()

        #only move the focused window if it is in the tiler
        if window in self.windows:

            i = self.windows.index(window)

            windowrest = self.windows[:i]
            windowrest.extend(self.windows[i+1:])

            #shift window location
            self.windows[0], self.windows[1:] = self.windows[i], windowrest 
            self.tile_windows()
 
    def decrease_masterarea_size(self):
        "Decreases the masterarea size by one"

        #decrease the masterarea size if it's possible
        if self.masterareaSize > 1:

            self.masterareaSize -= 1

            print ("masterarea size -= 1")
            self.tile_windows()

    def increase_masterarea_size(self):
        "Decreases the masterarea size by one"

        #increase the masterarea size if it's possible
        if self.masterareaSize < len(self.windows):

            self.masterareaSize += 1

            print ("masterarea size += 1")
            self.tile_windows()
   
