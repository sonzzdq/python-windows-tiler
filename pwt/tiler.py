import pwt.utilities

class Tiler(object):

    def __init__(self, rectangle):

        #rectangle
        #(left, top, right, bottom)
        self.left = rectangle[0]
        self.top = rectangle[1]

        self.width = rectangle[2] - rectangle[0]
        self.height = rectangle[3] - rectangle[1]

        self.masterareaWidth = self.width // 2
        self.masterareaSize = 1

        self.windows = []

    def merge_windows(self, newWindows):
        "Enumerateswindows, when the amount of windows changes it calls the handler, passing the current windows"

        reTile = False
        currentAmount = len(self.windows)
        newAmount = len(newWindows)

        #check for window changement
        if newAmount > currentAmount:

            for window in newWindows:

                if window not in self.windows:

                    self.windows.append(window)
                    reTile = True
                    print ("Add handle: ", window)

        elif currentAmount > newAmount:

            for window in self.windows:

                if window not in newWindows:

                    self.windows.remove(window)
                    reTile = True
                    print ("Remove handle: ", window)

        if reTile:

            #call the handler
            self.tile_windows()

    def tile_windows(self):
        "Tiles all windows, if windows are given it sets them to the self.windows attribute"

        if len(self.windows) > 1:

            #set the appropriate height depending on the amount of windows compared to the mastersize
            if self.masterareaSize == len(self.windows):

                height = self.height

            else:

                height = self.height // (len(self.windows) - self.masterareaSize)

            #set the appropriate height and width for the tile side
            if self.masterareaSize >= len(self.windows):

                heightMaster = self.height // len(self.windows)
                width = self.width

            else:

                heightMaster = self.height // self.masterareaSize
                width = self.masterareaWidth

            for i, window in enumerate(self.windows):

                if i in range(self.masterareaSize):

                    windowPosition = (self.left, self.top + i * heightMaster, width, heightMaster)

                else:

                    windowPosition = (self.left + width, self.top + (i - self.masterareaSize) * height, self.width - width, height)

                pwt.utilities.tile(window, windowPosition)

        elif len(self.windows) == 1:

            pwt.utilities.tile(self.windows[0], (self.left, self.top, self.width, self.height))

    ############################################
    ### Start of the commands
    ############################################

    def decrease_masterarea_width(self):
        "Decreases the masterarea width by 100px, else windows might overlap into different monitors and cause problems"

        if self.masterareaWidth >= 200:

            #decrease master areaWidth 
            self.masterareaWidth -= 100
            print("master area -= 100")

            self.tile_windows()

    def increase_masterarea_width(self):
        "Increases the masterarea width by 100px, else windows might overlap into different monitors and cause problems"

        if self.width - self.masterareaWidth >= 200:

            #increase master areaWidth 
            self.masterareaWidth += 100
            print("master area += 100")

            self.tile_windows()

    def set_focus_down(self):
        "Sets focus on the next window"

        #get focused window
        window = pwt.utilities.focused_window()

        #only grab and move the focus if it is in the self
        if window in self.windows:

            i = self.windows.index(window) + 1

            #if the index after the foreground's is out of range, assign 0
            if i >= len(self.windows):

                i = 0

            #focus window and cursor
            pwt.utilities.focus(self.windows[i])

        else:

            self.set_focus_to_masterarea()

    def set_focus_up(self):
        "Sets focus on the previous window"

        #get focused window
        window = pwt.utilities.focused_window()

        #only grab and move the focus if it is in the self
        if window in self.windows:

            i = self.windows.index(window) - 1

            #if the index before the foreground's is out of range, assign last index
            if i < 0:

                i = len(self.windows) - 1

            #focus window and cursor
            pwt.utilities.focus(self.windows[i])

        else:

            self.set_focus_to_masterarea()

    def set_focus_to_masterarea(self):
        "Sets focus on the masterarea"

        if len(self.windows):

            pwt.utilities.focus(self.windows[0])

    def move_focusedwindow_down(self):
        "Switches the window to the next position"
        
        #get focused window
        window = pwt.utilities.focused_window()

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

        window = pwt.utilities.focused_window()

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

        window = pwt.utilities.focused_window()

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
   
