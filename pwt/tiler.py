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

        self.masterareaCount = 1

        self.windows = []

        self.currentLayout = 0
        self.layouts = []

        self.layouts.append(Layout("Vertical"
            ,self.vertical_tile
            ,self.width))

        self.layouts.append(Layout("Horizontal"
            ,self.horizontal_tile
            ,self.height))

        self.masterarea = self.layouts[self.currentLayout].maxSize // 2

    def tile_windows(self):
        "Tiles all windows, if windows are given it sets them to the self.windows attribute"

        self.layouts[self.currentLayout].execute()

    ############################################
    ### Start of the commands
    ############################################

    def decrease_masterarea_width(self):
        "Decreases the masterarea width by 100px, else windows might overlap into different monitors and cause problems"

        if self.masterarea >= 200:

            #decrease master areaWidth 
            self.masterarea -= 100
            print("master area -= 100")

            self.tile_windows()

    def increase_masterarea_width(self):
        "Increases the masterarea width by 100px, else windows might overlap into different monitors and cause problems"

        if self.layouts[self.currentLayout].maxSize - self.masterarea >= 200:

            #increase master areaWidth 
            self.masterarea += 100
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

    def next_layout(self):
        "Switch to the next layout"

        if self.currentLayout >= len(self.layouts) - 1:

            self.currentLayout = 0

        else:

            self.currentLayout += 1

        self.masterarea = self.layouts[self.currentLayout].maxSize // 2
        self.tile_windows()

    ###
    # TILE LAYOUTS
    ###

    def vertical_tile(self):
        "Tiles the windows vertical"

        if len(self.windows):

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
                width = self.masterarea

            for i, window in enumerate(self.windows):

                #tile all master windows
                if i < self.masterareaCount:

                    windowLeft = self.left
                    windowTop = self.top + i * heightMaster

                    windowRight = self.left + width
                    windowBottom = self.top + (i + 1) * heightMaster

                #tile all the other windows
                else:

                    windowLeft = self.left + width
                    windowTop = self.top + (i - self.masterareaCount) * height

                    windowRight = self.left + self.width
                    windowBottom = self.top + (i - self.masterareaCount + 1) * height

                window.position((windowLeft
                    ,windowTop
                    ,windowRight
                    ,windowBottom))

    def horizontal_tile(self):
        "Tiles the windows horizontal"

        if len(self.windows):

            #set the appropriate width depending on the amount of windows compared to the mastersize
            if self.masterareaCount == len(self.windows):

                width = self.width

            else:

                width = self.width // (len(self.windows) - self.masterareaCount)

            #set the appropriate height and width for the tile side
            if self.masterareaCount >= len(self.windows):

                widthMaster = self.width // len(self.windows)
                height = self.height

            else:

                widthMaster = self.width // self.masterareaCount
                height = self.masterarea

            for i, window in enumerate(self.windows):

                #tile all master windows
                if i < self.masterareaCount:

                    windowLeft = self.left + i * widthMaster
                    windowTop = self.top 

                    windowRight = self.left + (i + 1) * widthMaster
                    windowBottom = self.top + height 

                #tile all the other windows
                else:

                    windowLeft = self.left + (i - self.masterareaCount) * width
                    windowTop = self.top + height 

                    windowRight = self.left + (i - self.masterareaCount + 1) * width
                    windowBottom = self.top + self.height 

                window.position((windowLeft
                    ,windowTop
                    ,windowRight
                    ,windowBottom))
