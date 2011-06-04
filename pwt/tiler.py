from pwt.window import Window
from pwt.layout import Layout

class Tiler(object):

    def __init__(self, rectangle, floats):

        self.floats = floats

        #rectangle
        #(left, top, right, bottom)
        self.left = rectangle[0]
        self.top = rectangle[1]

        self.width = rectangle[2] - rectangle[0]
        self.height = rectangle[3] - rectangle[1]

        self.masterareaSize = self.width // 2
        self.masterareaCount = 1

        self.windows = []

        self.currentLayout = 0
        self.layouts = []
        self.layouts.append(Layout("Vertical", self.vertical_tile))

    def tile_windows(self):
        "Tiles all windows, if windows are given it sets them to the self.windows attribute"

        self.layouts[self.currentLayout].execute()

    ############################################
    ### Start of the commands
    ############################################

    def decrease_masterarea_width(self):
        "Decreases the masterarea width by 100px, else windows might overlap into different monitors and cause problems"

        if self.masterareaSize >= 200:

            #decrease master areaWidth 
            self.masterareaSize -= 100
            print("master area -= 100")

            self.tile_windows()

    def increase_masterarea_width(self):
        "Increases the masterarea width by 100px, else windows might overlap into different monitors and cause problems"

        if self.width - self.masterareaSize >= 200:

            #increase master areaWidth 
            self.masterareaSize += 100
            print("master area += 100")

            self.tile_windows()

    def set_focus_down(self):
        "Sets focus on the next window"

        #get focused window
        window = Window.focused_window(self.floats)

        #only grab and move the focus if it is in the self
        if window in self.windows:

            i = self.windows.index(window) + 1

            #if the index after the foreground's is out of range, assign 0
            if i >= len(self.windows):

                i = 0

            #focus window and cursor
            self.windows[i].focus()

        else:

            self.set_focus_to_masterarea()

    def set_focus_up(self):
        "Sets focus on the previous window"

        #get focused window
        window = Window.focused_window(self.floats)

        #only grab and move the focus if it is in the self
        if window in self.windows:

            i = self.windows.index(window) - 1

            #if the index before the foreground's is out of range, assign last index
            if i < 0:

                i = len(self.windows) - 1

            #focus window and cursor
            self.windows[i].focus()

        else:

            self.set_focus_to_masterarea()

    def set_focus_to_masterarea(self):
        "Sets focus on the masterarea"

        if len(self.windows):

            self.windows[0].focus()

    def move_focusedwindow_down(self):
        "Switches the window to the next position"
        
        #get focused window
        window = Window.focused_window(self.floats)

        #only grab and move the window if it is in the self
        if window in self.windows:

            i = self.windows.index(window)

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

        window = Window.focused_window(self.floats)

        #only grab and move the window if it is in the self
        if window in self.windows:

            i = self.windows.index(window)

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

        window = Window.focused_window(self.floats)

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
        if self.masterareaCount > 1:

            self.masterareaCount -= 1

            print ("masterarea size -= 1")
            self.tile_windows()

    def increase_masterarea_size(self):
        "Decreases the masterarea size by one"

        #increase the masterarea size if it's possible
        if self.masterareaCount < len(self.windows):

            self.masterareaCount += 1

            print ("masterarea size += 1")
            self.tile_windows()


    ###
    # TILE LAYOUTS
    ###

    def vertical_tile(self):
        "Tiles the windows vertical"

        if len(self.windows) > 1:

            #set the appropriate height depending on the amount of windows compared to the mastersize
            if self.masterareaCount == len(self.windows):

                height = self.height

            else:

                height = self.height // (len(self.windows) - self.masterareaCount)

            #set the appropriate height and width for the tile side
            if self.masterareaCount >= len(self.windows):

                heightMaster = self.height // len(self.windows)
                width = self.width

            else:

                heightMaster = self.height // self.masterareaCount
                width = self.masterareaSize

            for i, window in enumerate(self.windows):

                if i in range(self.masterareaCount):

                    windowLeft = self.left
                    windowTop = self.top + i * heightMaster

                    windowWidth = self.left + width
                    windowHeight = self.top + (i + 1) * heightMaster

                else:

                    windowLeft = self.left + width
                    windowTop = self.top + (i - self.masterareaCount) * height

                    windowWidth = self.left + self.width
                    windowHeight = self.top + (i - self.masterareaCount + 1) * height

                window.position((windowLeft
                    ,windowTop
                    ,windowWidth
                    ,windowHeight))

        elif len(self.windows) == 1:

            windowLeft = self.left 
            windowTop = self.top

            windowWidth = self.left + self.width
            windowHeight = self.top + self.height 

            self.windows[0].position((windowLeft
                ,windowTop
                ,windowWidth
                ,windowHeight))
