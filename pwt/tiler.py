from pwt.layout     import Layout
from pwt.window     import Window
from pwt.utility    import Utility

class Tiler(object):

    def __init__(self, workarea):

        self.calc_dimensions(workarea)

        self.layouts = []

        self.layouts.append(Layout("Vertical"
            ,self.vertical_tile
            ,self.width
        ))

        self.layouts.append(Layout("Horizontal"
            ,self.horizontal_tile
            ,self.height
        ))

        self.layouts.append(Layout("Fullscreen"
            ,self.fullscreen_tile
            ,1
        ))

        self.currentLayout = self.layouts[0]

        self.masterarea = self.currentLayout.maxSize // 2
        self.masterareaCount = 1

        self.windows = []

    def calc_dimensions(self,workarea):

        #rectangle
        #(left, top, right, bottom)
        self.left = workarea[0]
        self.top = workarea[1]

        self.width = workarea[2] - workarea[0]
        self.height = workarea[3] - workarea[1]

    def tile_windows(self):
        """
        Tiles all windows by feeding it to the layout
        """

        self.currentLayout.execute()

    def remove_window(self, window):
        """
        Removes the window from the list and retiles the setup
        """

        self.windows.remove(window)
        self.tile_windows()

    def add_window(self, window):
        """
        Adds the window to the list and retiles the setup
        """

        self.windows.append(window)
        self.tile_windows()


    ############################################
    ### Start of the commands
    ############################################

    def decrease_masterarea(self):
        """
        Decreases the masterarea width by 100px 
        Sets a border at 200px else windows might overlap 
        into different monitors and cause problems
        """

        if self.masterarea >= 200:

            #decrease master areaWidth 
            self.masterarea -= 100

            self.tile_windows()

    def increase_masterarea(self):
        """
        Increases the masterarea width by 100px
        Sets a borderat 200px else windows might overlap 
        into different monitors and cause problems
        """

        if self.currentLayout.maxSize - self.masterarea >= 200:

            #increase master areaWidth 
            self.masterarea += 100

            self.tile_windows()

    def focus_next(self):
        """
        Sets focus on the next window
        """

        window = Utility.next_item(self.windows, Window.focused_window())

        if window:            
            
            if not window.focus():

                self.remove_window(window)

        else:

            self.focus_primary()

    def focus_previous(self):
        """
        Sets focus on the previous window
        """

        #get focused window
        window = Utility.previous_item(self.windows, Window.focused_window())

        if window: 

            if not window.focus():

                self.remove_window(window)

        else:

            self.focus_primary()

    def focus_primary(self):
        """
        Sets focus on the first window
        """

        if len(self.windows):

            if not self.windows[0].focus():

                del self.windows[0]
                self.tile_windows()

    def move_focused_to_next(self):
        """
        Switches the window to the next position
        """
        
        #get focused window
        window = Window.focused_window()

        #only grab and move the window if it is in the self
        if window in self.windows:

            i = self.windows.index(window)

            #if the foreground window is the last window, shift everything and place it first
            if i == len(self.windows) - 1:

                self.windows[0], self.windows[1:] = self.windows[i], self.windows[:i]

            #else shift it with the following window
            else:

                self.windows[i], self.windows[i+1] = self.windows[i+1], self.windows[i]

            self.tile_windows()

            if not window.focus():

                self.remove_window(window)

    def move_focused_to_previous(self):
        """
        Switches the window to the previous position
        """

        window = Window.focused_window()

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

            self.tile_windows()

            if not window.focus():

                self.remove_window(window)

    def make_focused_primary(self):
        """
        Moves the focused window to the first place in the masterarea
        """

        window = Window.focused_window()

        #only move the focused window if it is in the tiler
        if window in self.windows:

            i = self.windows.index(window)

            windowrest = self.windows[:i]
            windowrest.extend(self.windows[i+1:])

            #shift window location
            self.windows[0], self.windows[1:] = self.windows[i], windowrest 
            self.tile_windows()

            if not window.focus():

                self.remove_window(window)

    def increase_masterarea_size(self):
        """
        Increase the masterarea size by one
        """

        #increase the masterarea size if it's possible
        if self.masterareaCount < len(self.windows):

            self.masterareaCount += 1

            self.tile_windows()

    def decrease_masterarea_size(self):
        """
        Decreases the masterarea size by one
        """

        #decrease the masterarea size if it's possible
        if self.masterareaCount > 1:

            self.masterareaCount -= 1

            self.tile_windows()

    def next_layout(self):
        """
        Switch to the next layout
        """
        
        nextLayout = Utility.next_item(self.layouts, self.currentLayout) 

        if nextLayout: 

            self.currentLayout = nextLayout

        self.masterarea = self.currentLayout.maxSize // 2

        self.tile_windows()

        if not Window.focused_window().center_cursor():

            self.remove_window(window)

    ###
    # TILE LAYOUTS
    ###

    def vertical_tile(self):
        """
        "Tiles the windows vertical"
        """

        if len(self.windows):

            #set the appropriate height depending
            #on the amount of windows compared to the mastersize
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

                position = (windowLeft 
                        ,windowTop 
                        ,windowRight 
                        ,windowBottom)

                if not window.position(position):

                    self.remove_window(window)

                    self.tile_windows()

                    break

    def horizontal_tile(self):
        """
        "Tiles the windows horizontal"
        """

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

                position = (windowLeft 
                        ,windowTop 
                        ,windowRight 
                        ,windowBottom)

                if not window.position(position):

                    self.remove_window(window)

                    self.tile_windows()

                    break

    def fullscreen_tile(self):
        """
        "Tiles all windows in fullscreen"
        """
        
        for window in self.windows:

            position = (self.left
                ,self.top
                ,self.left + self.width
                ,self.top + self.height)

            if not window.position(position):

                self.remove_window(window)

                self.tile_windows()

                break
