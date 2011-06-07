##PWT specific imports
from pwt.hotkeycontroller import HotkeyController
from pwt.windowcaller import WindowCaller
from pwt.tiler import Tiler
from pwt.systrayicon import SysTrayIcon
from pwt.window import Window
import pwt.utilities

##Import needed python modules 
import glob
import time

##KEYS
from win32con import MOD_ALT
from win32con import MOD_SHIFT
from win32con import VK_RETURN
from win32con import VK_DELETE
from win32con import VK_SPACE

##HOTKEY EVENTS
from win32con import WM_HOTKEY

##TILE EVENTS
from win32con import HSHELL_WINDOWCREATED
from win32con import HSHELL_WINDOWDESTROYED

class Controller(object):

    def __init__(self):
        "create the hotkey and window listeners on initialization"

        self.ICONFOLDER = "icons/"

        self.WINDOWCLASSNAME = "PWT"

        self.NAME = "PWT"

        #create <<classname>> based ignorelist
        self.FLOATS = (#This list may hurt performance if it's huge
                "#32770"#Task manager
               ,"progman"#Desktop
                )

        #the events that trigger the removal of a window
        self.REMOVE_EVENTS = (HSHELL_WINDOWDESTROYED
                ,#placeholder
                )

        #the events that trigger an additional window
        self.ADD_EVENTS = (HSHELL_WINDOWCREATED
                ,#placeholder
                )

        #list the HOTKEYS that should be listened to
        self.HOTKEYS = {1: (MOD_ALT, ord("H"))
                , 2: (MOD_ALT, ord("L"))
                , 3: (MOD_ALT, ord("J"))
                , 4: (MOD_ALT, ord("K"))
                , 5: (MOD_ALT, VK_RETURN)
                , 6: (MOD_ALT + MOD_SHIFT, ord("J"))
                , 7: (MOD_ALT + MOD_SHIFT, ord("K"))
                , 8: (MOD_ALT + MOD_SHIFT, VK_RETURN)
                , 9: (MOD_ALT + MOD_SHIFT, ord("L"))
                , 10: (MOD_ALT + MOD_SHIFT, ord("H"))
                , 11: (MOD_ALT + MOD_SHIFT, ord("C"))
                , 12: (MOD_ALT, ord("1"))
                , 13: (MOD_ALT, ord("2"))
                , 14: (MOD_ALT, ord("3"))
                , 15: (MOD_ALT, ord("4"))
                , 16: (MOD_ALT, ord("5"))
                , 17: (MOD_ALT, ord("6"))
                , 18: (MOD_ALT, ord("7"))
                , 19: (MOD_ALT, ord("8"))
                , 20: (MOD_ALT, ord("9"))
                , 21: (MOD_ALT + MOD_SHIFT, ord("1"))
                , 22: (MOD_ALT + MOD_SHIFT, ord("2"))
                , 23: (MOD_ALT + MOD_SHIFT, ord("3"))
                , 24: (MOD_ALT + MOD_SHIFT, ord("4"))
                , 25: (MOD_ALT + MOD_SHIFT, ord("5"))
                , 26: (MOD_ALT + MOD_SHIFT, ord("6"))
                , 27: (MOD_ALT + MOD_SHIFT, ord("7"))
                , 28: (MOD_ALT + MOD_SHIFT, ord("8"))
                , 29: (MOD_ALT + MOD_SHIFT, ord("9"))
                , 30: (MOD_ALT, ord("I"))
                , 31: (MOD_ALT, ord("U"))
                , 32: (MOD_ALT + MOD_SHIFT, ord("I"))
                , 33: (MOD_ALT + MOD_SHIFT, ord("U"))
                , 34: (MOD_ALT + MOD_SHIFT, ord("D"))
                , 35: (MOD_ALT, VK_SPACE)
                , 36: (MOD_ALT + MOD_SHIFT, VK_DELETE)
                }

        #list the corresponding self.handlers 
        self.HOTKEYHANDLERS = {1: self.handler_alt_H
                , 2:  self.handler_alt_L
                , 3:  self.handler_alt_J
                , 4:  self.handler_alt_K
                , 5:  self.handler_alt_return
                , 6:  self.handler_alt_shift_J
                , 7:  self.handler_alt_shift_K
                , 8:  self.handler_alt_shift_return
                , 9:  self.handler_alt_shift_L
                , 10:  self.handler_alt_shift_H
                , 11:  self.handler_alt_shift_C
                , 12:  self.handler_alt_one
                , 13:  self.handler_alt_two
                , 14:  self.handler_alt_three
                , 15:  self.handler_alt_four
                , 16:  self.handler_alt_five
                , 17:  self.handler_alt_six
                , 18:  self.handler_alt_seven
                , 19:  self.handler_alt_eight
                , 20:  self.handler_alt_nine
                , 21:  self.handler_alt_shift_one
                , 22:  self.handler_alt_shift_two
                , 23:  self.handler_alt_shift_three
                , 24:  self.handler_alt_shift_four
                , 25:  self.handler_alt_shift_five
                , 26:  self.handler_alt_shift_six
                , 27:  self.handler_alt_shift_seven
                , 28:  self.handler_alt_shift_eight
                , 29:  self.handler_alt_shift_nine
                , 30:  self.handler_alt_I
                , 31:  self.handler_alt_U
                , 32:  self.handler_alt_shift_I
                , 33:  self.handler_alt_shift_U
                , 34:  self.handler_alt_shift_D
                , 35:  self.handler_alt_space
                , 36:  self.handler_alt_shift_delete
                }

        #Create a dictionary mapping 9 tilers per monitor
        self.monitorTilers = {}
        self.workspace = 0

        #For each monitor, create a monitorTiler dict item containing monitor:tilerList
        for monitorTuple in pwt.utilities.display_monitors(): 

            tilers = []

            for i in range(9):

                monitorWorkArea = pwt.utilities.monitor_workrectangle(monitorTuple[0])
                tilers.append(Tiler(monitorWorkArea, self.FLOATS))

            self.monitorTilers[int(monitorTuple[0])] = tilers 
            print("Monitor:", monitorTuple[0])

        #Create systrayicon
        self.systrayicon = SysTrayIcon(self.icon()
                ,self.NAME
                ,self.WINDOWCLASSNAME)

        #Create a dummy window to register hooks to 
        self.hwnd = self.systrayicon.hwnd
        
        #Register a shellhook for the window
        pwt.utilities.register_shellhook(self.hwnd) 
                
        #Create the hotkeycontroller with the hotkeys, handlers and window
        self.hotkeycontroller = HotkeyController(self.HOTKEYS
                ,self.HOTKEYHANDLERS
                ,self.hwnd)

        #Register hotkeys
        self.hotkeycontroller.register_hotkeys()

        self.stop = False

    def icon(self):
        "Return the appropriate icon"

        return self.ICONFOLDER + str(self.workspace + 1) + ".ico"

    def current_tiler(self):
        "Return current tiler"

        return self.current_tilers()[self.workspace]

    def current_tilers(self):
        "Return current tilers"

        return self.monitorTilers[pwt.utilities.current_monitor()]

    ###
    #Commands
    ###

    def start(self):
        "start the listeners with a safety try/finally to unregister keys and kill the icon"

        #Do an initial lookup of all the windows and tile accordingly
        self.initial_tile()

        try:

            #message priming read
            message = pwt.utilities.windowmessage(self.hwnd) 

            print(message)
            while message:

                #if message is WM_HOTKEY
                if message[1][1] == WM_HOTKEY:

                    #execute the corresponding hotkeyhandler
                    self.HOTKEYHANDLERS[message[1][2]]()

                #if lparam is a tile event
                elif message[1][2] in self.ADD_EVENTS:

                    self.handle_add_event(Window(message[1][3], self.FLOATS))
                    
                #if lparam is a remove event
                elif message[1][2] in self.REMOVE_EVENTS:

                    self.handle_remove_event(Window(message[1][3], self.FLOATS)
                            ,pwt.utilities.monitor_from_point(message[1][5]))

                if self.stop:

                    break

                #Grab the next message from the self.hwnd message queue
                message = pwt.utilities.windowmessage(self.hwnd) 

        finally:

            #Unregister hotkeys and shellhook
            self.hotkeycontroller.unregister_hotkeys()
            pwt.utilities.unregister_shellhook(self.hwnd)

            #Decorate windows
            self.decorate_all_tiledwindows()

            #Remove systrayicon
            self.systrayicon.destroy()

    def handle_add_event(self, window):
        "Triggered when a window has to be added"

        #Check for the floating list
        if window.classname() not in self.FLOATS:

            tiler = self.current_tiler()

            #if it should be tiled and isn't already tiled
            if window.should_tile() and window not in tiler.windows:
                
                #undecorate and update the window
                window.undecorate()
                window.update()

                #append and tile retile the windows
                tiler.windows.append(window)
                tiler.tile_windows()

    def handle_remove_event(self, window, monitor):
        "Triggered when a window needs to be removed"


        tiler = self.monitorTilers[monitor][self.workspace]

        if window in tiler.windows:

            tiler.windows.remove(window)
            tiler.tile_windows()

    def decorate_all_tiledwindows(self):
        "Decorates all windows in the tiler's memory"

        for tilers in self.monitorTilers.values():

            for tiler in tilers:

                for window in tiler.windows:

                    window.decorate()
                    window.update()
                    window.show()


    def initial_tile(self):
        "Controls and handles all the windows on the screen, merging the changes with the tilers"

        #Create a caller
        self.windowcaller = WindowCaller(self.FLOATS)

        #Do a tile for each monitor
        for monitor, tilers in self.monitorTilers.items():

            tilers[self.workspace].windows = self.windowcaller.windows_for_monitor(monitor)

            tilers[self.workspace].tile_windows()

    def switch_workspace(self, i):
        "Switch the current workspace into workspace i"

        allCurrentWindows = []
        allNewWindows = []

        #Make a set of all the windows in the current workspace
        for tilers in self.monitorTilers.values():

            allCurrentWindows.extend(tilers[self.workspace].windows)

        #Make a set of all the windows in the new workspace
        for tilers in self.monitorTilers.values():

            allNewWindows.extend(tilers[i].windows)

        #Hide all windows that aren't in the new workspace
        for window in set(allCurrentWindows) - set(allNewWindows):

            window.hide()

        #Show all windows that weren't in the current workspace
        for window in set(allNewWindows) - set(allCurrentWindows):

            window.show()

        #Retile all tilers in the current workspace
        for tilers in self.monitorTilers.values():

            tilers[i].tile_windows()

        self.workspace = i
        self.systrayicon.refresh_icon(self.icon())

        window = Window.window_under_cursor(self.FLOATS)

        if window:

            window.focus()

    def send_window_to_tiler(self, window, i):
        "sends window to tiler i"

        currentTilers = self.current_tilers()
        currentTiler = self.current_tiler()

        #hide the window
        if window.should_tile():

            window.hide()

            #Remove window if it's in the tiler
            if window in currentTiler.windows:

                currentTiler.windows.remove(window)
                currentTiler.tile_windows()

            #Add window if it's not already in the target tiler
            if window not in currentTilers[i].windows:

                currentTilers[i].windows.append(window)

    ###
    #Hotkey handlers
    ###

    def handler_alt_H(self):
        "Handles alt+H, decreases the masterwidth"

        self.current_tiler().decrease_masterarea_width()

    def handler_alt_L(self):
        "Handles alt+L, increases the masterwidth"

        self.current_tiler().increase_masterarea_width()

    def handler_alt_J(self):
        "Handles alt+J, sets focus on the next window"

        self.current_tiler().set_focus_down()

    def handler_alt_K(self):
        "Handles alt+K, sets focus on the previous window"

        self.current_tiler().set_focus_up()

    def handler_alt_return(self):
        "Handles alt+RETURN, sets focus on the masterarea"

        self.current_tiler().set_focus_to_masterarea()

    def handler_alt_shift_J(self):
        "Handles alt+shift+J, switches the window to the next position"

        self.current_tiler().move_focusedwindow_down()

    def handler_alt_shift_K(self):
        "Handles alt+shift+K, switches the window to the previous position"

        self.current_tiler().move_focusedwindow_up()

    def handler_alt_shift_return(self):
        "Handles alt+shift+RETURN, switches the window to the masterarea"

        self.current_tiler().move_focusedwindow_to_masterarea()

    def handler_alt_shift_L(self):
        "Handles alt+shift+L, decreases the masterarea size"

        self.current_tiler().decrease_masterarea_size()

    def handler_alt_shift_H(self):
        "Handles alt+shift+H, increases the masterarea size"

        self.current_tiler().increase_masterarea_size()

    def handler_alt_shift_C(self):
        "Handles alt+shift+C, closes the current window"

        Window.focused_window(self.FLOATS).close()

    def handler_alt_one(self):
        "Handles alt+1, switches workspace"
        
        if self.workspace != 0:

            self.switch_workspace(0)

    def handler_alt_two(self):
        "Handles alt+2, switches workspace"
        
        if self.workspace != 1:

            self.switch_workspace(1)

    def handler_alt_three(self):
        "Handles alt+3, switches workspace"
        
        if self.workspace != 2:

            self.switch_workspace(2)

    def handler_alt_four(self):
        "Handles alt+4, switches workspace"
        
        if self.workspace != 3:

            self.switch_workspace(3)

    def handler_alt_five(self):
        "Handles alt+5, switches workspace"
        
        if self.workspace != 4:

            self.switch_workspace(4)

    def handler_alt_six(self):
        "Handles alt+6, switches workspace"
        
        if self.workspace != 5:

            self.switch_workspace(5)

    def handler_alt_seven(self):
        "Handles alt+7, switches workspace"
        
        if self.workspace != 6:

            self.switch_workspace(6)

    def handler_alt_eight(self):
        "Handles alt+8, switches workspace"
        
        if self.workspace != 7:

            self.switch_workspace(7)

    def handler_alt_nine(self):
        "Handles alt+9, switches workspace"
        
        if self.workspace != 8:

            self.switch_workspace(8)

    def handler_alt_shift_one(self):
        "Handles alt+shift+1, sends window to appropriate tiler"

        if self.workspace != 0:

            window = Window.focused_window(self.FLOATS) 

            if window:

                self.send_window_to_tiler(window, 0)

    def handler_alt_shift_two(self):
        "Handles alt+shift+2, sends window to appropriate tiler"

        if self.workspace != 1:

            window = Window.focused_window(self.FLOATS) 

            if window:

                self.send_window_to_tiler(window, 1)

    def handler_alt_shift_three(self):
        "Handles alt+shift+3, sends window to appropriate tiler"

        if self.workspace != 2:

            window = Window.focused_window(self.FLOATS) 

            if window:

                self.send_window_to_tiler(window, 2)

    def handler_alt_shift_four(self):
        "Handles alt+shift+4, sends window to appropriate tiler"

        if self.workspace != 3:

            window = Window.focused_window(self.FLOATS) 

            if window:

                self.send_window_to_tiler(window, 3)

    def handler_alt_shift_five(self):
        "Handles alt+shift+5, sends window to appropriate tiler"

        if self.workspace != 4:

            window = Window.focused_window(self.FLOATS) 

            if window:

                self.send_window_to_tiler(window, 4)

    def handler_alt_shift_six(self):
        "Handles alt+shift+6, sends window to appropriate tiler"

        if self.workspace != 5:

            window = Window.focused_window(self.FLOATS) 

            if window:

                self.send_window_to_tiler(window, 5)

    def handler_alt_shift_seven(self):
        "Handles alt+shift+7, sends window to appropriate tiler"

        if self.workspace != 6:

            window = Window.focused_window(self.FLOATS) 

            if window:

                self.send_window_to_tiler(window, 6)

    def handler_alt_shift_eight(self):
        "Handles alt+shift+8, sends window to appropriate tiler"

        if self.workspace != 7:

            window = Window.focused_window(self.FLOATS) 

            if window:

                self.send_window_to_tiler(window, 7)

    def handler_alt_shift_nine(self):
        "Handles alt+shift+9, sends window to appropriate tiler"

        if self.workspace != 8:

            window = Window.focused_window(self.FLOATS) 

            if window:

                self.send_window_to_tiler(window, 8)

    def handler_alt_I(self):
        "Handles alt+F, changes focus to the next monitor"

        monitor = pwt.utilities.current_monitor()
        monitors = list(self.monitorTilers.keys())

        if monitor in monitors:

            i = monitors.index(monitor) + 1

            if i >= len(monitors):

                    i = 0

            if len(self.monitorTilers[monitors[i]][self.workspace].windows):

                #Focus the first window in the current workspace of the next monitor in the monitorTiler dict
                self.monitorTilers[monitors[i]][self.workspace].windows[0].focus()

        else:

            self.monitorTilers[pwt.utilities.main_monitor()][self.workspace].windows[0].focus()

    def handler_alt_U(self):
        "Handles alt+F, changes focus to the previous monitor"

        monitor = pwt.utilities.current_monitor()
        monitors = list(self.monitorTilers.keys())

        if monitor in monitors:

            i = monitors.index(monitor) - 1

            if i < 0:

                    i = len(monitors) - 1

            if len(self.monitorTilers[monitors[i]][self.workspace].windows):

                #Focus the first window in the current workspace of the previous monitor in the monitorTiler dict
                self.monitorTilers[monitors[i]][self.workspace].windows[0].focus()

        else:

            self.monitorTilers[pwt.utilities.main_monitor()][self.workspace].windows[0].focus()

    def handler_alt_shift_I(self):
        "Handles alt+shft_I switches window to the next monitor"

        window = Window.focused_window(self.FLOATS)
        monitor = pwt.utilities.current_monitor()
        monitors = list(self.monitorTilers.keys())

        if monitor in monitors:

            i = monitors.index(monitor) + 1

            if i >= len(monitors):

                    i = 0

            currentTiler = self.monitorTilers[monitor][self.workspace]
            targetTiler = self.monitorTilers[monitors[i]][self.workspace]
            
            if window in currentTiler.windows:

                currentTiler.windows.remove(window)
                currentTiler.tile_windows()

            if window not in targetTiler.windows:

                targetTiler.windows.append(window)
                targetTiler.tile_windows()

            window.focus()

    def handler_alt_shift_U(self):
        "Handles alt+shft_U switches window to the previous monitor"

        window = Window.focused_window(self.FLOATS)
        monitor = pwt.utilities.current_monitor()
        monitors = list(self.monitorTilers.keys())

        if monitor in monitors:

            i = monitors.index(monitor) - 1

            if i < 0:

                    i = len(monitors) - 1

            currentTiler = self.monitorTilers[monitor][self.workspace]
            targetTiler = self.monitorTilers[monitors[i]][self.workspace]
            
            if window in currentTiler.windows:

                currentTiler.windows.remove(window)
                currentTiler.tile_windows()

            if window not in targetTiler.windows:

                targetTiler.windows.append(window)
                targetTiler.tile_windows()

            window.focus()

    def handler_alt_space(self):
        "Handles alt+space, grabs the next tile layout"

        self.current_tiler().next_layout()

    def handler_alt_shift_D(self):
        "Handles alt+shift+D, toggles decorations"

        window = Window.focused_window(self.FLOATS)

        if window:

            if window.should_tile():

                if window.has_decorations():

                    window.undecorate()

                else:

                    window.decorate()

                window.update()

    def handler_alt_shift_delete(self):
        "Handles alt+shift+end, quits the listening"
        
        #stop the polling
        self.stop = True

