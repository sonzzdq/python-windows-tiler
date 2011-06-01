from pwt.hotkeylistener import HotkeyListener
from pwt.windowcaller import WindowCaller
from pwt.tiler import Tiler
from pwt.systrayicon import SysTrayIcon

import glob
import time
import pwt.utilities
import win32api

from win32con import MOD_ALT
from win32con import MOD_SHIFT
from win32con import VK_RETURN

class Controller(object):

    def __init__(self):
        "create the hotkey and window listeners on initialization"

        self.ICONFOLDER = "icons/"
        #create <<classname>> based ignorelist
        self.FLOATS = (#This list may hurt performance if it's huge
                #"progman"			#example
                #, "progman"		#example
                )

        #list the HOTKEYS that should be listened to
        HOTKEYS = {1: (MOD_ALT, ord("H"))
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
                , 12: (MOD_ALT + MOD_SHIFT, ord("V"))
                , 13: (MOD_ALT, ord("1"))
                , 14: (MOD_ALT, ord("2"))
                , 15: (MOD_ALT, ord("3"))
                , 16: (MOD_ALT, ord("4"))
                , 17: (MOD_ALT, ord("5"))
                , 18: (MOD_ALT, ord("6"))
                , 19: (MOD_ALT, ord("7"))
                , 20: (MOD_ALT, ord("8"))
                , 21: (MOD_ALT, ord("9"))
                , 22: (MOD_ALT + MOD_SHIFT, ord("1"))
                , 23: (MOD_ALT + MOD_SHIFT, ord("2"))
                , 24: (MOD_ALT + MOD_SHIFT, ord("3"))
                , 25: (MOD_ALT + MOD_SHIFT, ord("4"))
                , 26: (MOD_ALT + MOD_SHIFT, ord("5"))
                , 27: (MOD_ALT + MOD_SHIFT, ord("6"))
                , 28: (MOD_ALT + MOD_SHIFT, ord("7"))
                , 29: (MOD_ALT + MOD_SHIFT, ord("8"))
                , 30: (MOD_ALT + MOD_SHIFT, ord("9"))
                , 31: (MOD_ALT, ord("F"))
                , 32: (MOD_ALT, ord("D"))
                , 33: (MOD_ALT + MOD_SHIFT, ord("F"))
                , 34: (MOD_ALT + MOD_SHIFT, ord("D"))
                , 35: (MOD_ALT + MOD_SHIFT, ord("Q"))
                }

        #list the corresponding self.handlers 
        HOTKEYHANDLERS = {1: self.handler_alt_H
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
                , 12:  self.handler_alt_shift_V
                , 13:  self.handler_alt_one
                , 14:  self.handler_alt_two
                , 15:  self.handler_alt_three
                , 16:  self.handler_alt_four
                , 17:  self.handler_alt_five
                , 18:  self.handler_alt_six
                , 19:  self.handler_alt_seven
                , 20:  self.handler_alt_eight
                , 21:  self.handler_alt_nine
                , 22:  self.handler_alt_shift_one
                , 23:  self.handler_alt_shift_two
                , 24:  self.handler_alt_shift_three
                , 25:  self.handler_alt_shift_four
                , 26:  self.handler_alt_shift_five
                , 27:  self.handler_alt_shift_six
                , 28:  self.handler_alt_shift_seven
                , 29:  self.handler_alt_shift_eight
                , 30:  self.handler_alt_shift_nine
                , 31:  self.handler_alt_F
                , 32:  self.handler_alt_D
                , 33:  self.handler_alt_shift_F
                , 34:  self.handler_alt_shift_D
                , 35:  self.handler_alt_shift_Q
                }

        self.stop = False

        #Create the listeners
        self.hotkeylistener = HotkeyListener(HOTKEYS, HOTKEYHANDLERS)

        #Create a dictionary mapping 9 tilers per monitor
        self.monitorTilers = {}
        self.currentWorkspace = 0

        for monitorTuple in win32api.EnumDisplayMonitors():

            tilers = []

            for i in range(9):

                tilers.append(Tiler(pwt.utilities.get_monitor_workrectangle(monitorTuple[0])))

            self.monitorTilers[int(monitorTuple[0])] = tilers 

        print(self.monitorTilers.keys())

    def icon(self):
        "Return the appropriate icon"

        return self.ICONFOLDER + str(self.currentWorkspace + 1) + ".ico"

    def current_tiler(self):
        "Return current tiler"

        return self.current_tilers()[self.currentWorkspace]

    def current_tilers(self):
        "Return current tilers"

        return self.monitorTilers[pwt.utilities.current_monitor()]

    ###
    #Commands
    ###

    def start(self):
        "start the listeners with a safety try/finally to unregister keys and kill the icon"

        print("start")

        #Register hotkeys
        self.hotkeylistener.register_hotkeys()

        #Create systrayicon
        self.systrayicon = SysTrayIcon(self.icon(), "PWT", "PWT")

        try:

            while not self.stop:

                #Sleep for 0.05 to save resources
                time.sleep(0.05)

                windowcaller = WindowCaller(self.FLOATS)

                for monitor, tilers in self.monitorTilers.items():

                    tilers[self.currentWorkspace].merge_windows(windowcaller.windows_for_monitor(monitor))

                #Use the listeners
                self.hotkeylistener.listen_to_keys()

        finally:

            print("stop")

            #Unregister hotkeys
            self.hotkeylistener.unregister_hotkeys()

            #Remove systrayicon
            self.systrayicon.destroy()


    def switch_workspace(self, i):
        "Switch the current workspace into workspace i"

        allCurrentWindows = []
        allNewWindows = []

        #Make a set of all the windows in the current workspace
        for tilers in self.monitorTilers.values():

            allCurrentWindows.extend(tilers[self.currentWorkspace].windows)

        #Make a set of all the windows in the new workspace
        for tilers in self.monitorTilers.values():

            allNewWindows.extend(tilers[i].windows)

        #Minimize all windows that aren't in the new workspace
        for window in set(allCurrentWindows) - set(allNewWindows):

            pwt.utilities.minimize(window)

        #Show all windows that weren't in the current workspace
        for window in set(allNewWindows) - set(allCurrentWindows):

            pwt.utilities.show(window)

        #Minize all windows that aren't in the next tiler
        for tilers in self.monitorTilers.values():

            #Tile the windows from the target tiler and reload the appropriate settings
            tilers[i].tile_windows()

        self.currentWorkspace = i
        self.systrayicon.refresh_icon(self.icon())

    def send_window_to_tiler(self, window, i):
        "Sends window to tiler i"

        currentTilers = self.current_tilers()

        #Minimize the window
        pwt.utilities.minimize(window)

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

        window = pwt.utilities.focused_window()

        pwt.utilities.close(window)

    def handler_alt_shift_V(self):
        "Handles alt+shift+V, minimizes the current window"

        window = pwt.utilities.focused_window()

        pwt.utilities.minimize(window)

    def handler_alt_one(self):
        "Handles alt+1, switches workspace"
        
        if self.currentWorkspace != 0:

            self.switch_workspace(0)

    def handler_alt_two(self):
        "Handles alt+2, switches workspace"
        
        if self.currentWorkspace != 1:

            self.switch_workspace(1)

    def handler_alt_three(self):
        "Handles alt+3, switches workspace"
        
        if self.currentWorkspace != 2:

            self.switch_workspace(2)

    def handler_alt_four(self):
        "Handles alt+4, switches workspace"
        
        if self.currentWorkspace != 3:

            self.switch_workspace(3)

    def handler_alt_five(self):
        "Handles alt+5, switches workspace"
        
        if self.currentWorkspace != 4:

            self.switch_workspace(4)

    def handler_alt_six(self):
        "Handles alt+6, switches workspace"
        
        if self.currentWorkspace != 5:

            self.switch_workspace(5)

    def handler_alt_seven(self):
        "Handles alt+7, switches workspace"
        
        if self.currentWorkspace != 6:

            self.switch_workspace(6)

    def handler_alt_eight(self):
        "Handles alt+8, switches workspace"
        
        if self.currentWorkspace != 7:

            self.switch_workspace(7)

    def handler_alt_nine(self):
        "Handles alt+9, switches workspace"
        
        if self.currentWorkspace != 8:

            self.switch_workspace(8)

    def handler_alt_shift_one(self):
        "Handles alt+shift+1, sends window to appropriate tiler"

        if self.currentWorkspace != 0:

            window = pwt.utilities.focused_window() 

            if window:

                self.send_window_to_tiler(window, 0)

    def handler_alt_shift_two(self):
        "Handles alt+shift+2, sends window to appropriate tiler"

        if self.currentWorkspace != 1:

            window = pwt.utilities.focused_window() 

            if window:

                self.send_window_to_tiler(window, 1)

    def handler_alt_shift_three(self):
        "Handles alt+shift+3, sends window to appropriate tiler"

        if self.currentWorkspace != 2:

            window = pwt.utilities.focused_window() 

            if window:

                self.send_window_to_tiler(window, 2)

    def handler_alt_shift_four(self):
        "Handles alt+shift+4, sends window to appropriate tiler"

        if self.currentWorkspace != 3:

            window = pwt.utilities.focused_window() 

            if window:

                self.send_window_to_tiler(window, 3)

    def handler_alt_shift_five(self):
        "Handles alt+shift+5, sends window to appropriate tiler"

        if self.currentWorkspace != 4:

            window = pwt.utilities.focused_window() 

            if window:

                self.send_window_to_tiler(window, 4)

    def handler_alt_shift_six(self):
        "Handles alt+shift+6, sends window to appropriate tiler"

        if self.currentWorkspace != 5:

            window = pwt.utilities.focused_window() 

            if window:

                self.send_window_to_tiler(window, 5)

    def handler_alt_shift_seven(self):
        "Handles alt+shift+7, sends window to appropriate tiler"

        if self.currentWorkspace != 6:

            window = pwt.utilities.focused_window() 

            if window:

                self.send_window_to_tiler(window, 6)

    def handler_alt_shift_eight(self):
        "Handles alt+shift+8, sends window to appropriate tiler"

        if self.currentWorkspace != 7:

            window = pwt.utilities.focused_window() 

            if window:

                self.send_window_to_tiler(window, 7)

    def handler_alt_shift_nine(self):
        "Handles alt+shift+9, sends window to appropriate tiler"

        if self.currentWorkspace != 8:

            window = pwt.utilities.focused_window() 

            if window:

                self.send_window_to_tiler(window, 8)

    def handler_alt_F(self):
        "Handles alt+F, changes focus to the next monitor"

        monitor = pwt.utilities.current_monitor()
        monitors = list(self.monitorTilers.keys())

        if monitor in monitors:

            i = monitors.index(monitor) + 1

            if i >= len(monitors):

                    i = 0

            #Focus the first window in the current workspace of the next monitor in the monitorTiler dict
            pwt.utilities.focus(self.monitorTilers[monitors[i]][self.currentWorkspace].windows[0])

        else:

            pwt.utilities.focus(self.monitorTilers[monitors[0]][self.currentWorkspace].windows[0])

    def handler_alt_D(self):
        "Handles alt+F, changes focus to the previous monitor"

        monitor = pwt.utilities.current_monitor()
        monitors = list(self.monitorTilers.keys())

        if monitor in monitors:

            i = monitors.index(monitor) - 1

            if i < 0:

                    i = len(monitors) - 1

            #Focus the first window in the current workspace of the previous monitor in the monitorTiler dict
            pwt.utilities.focus(self.monitorTilers[monitors[i]][self.currentWorkspace].windows[0])

        else:

            pwt.utilities.focus(self.monitorTilers[monitors[0]][self.currentWorkspace].windows[0])

    def handler_alt_shift_F(self):

        window = pwt.utilities.focused_window()
        monitor = pwt.utilities.current_monitor()
        monitors = list(self.monitorTilers.keys())

        if monitor in monitors:

            i = monitors.index(monitor) + 1

            if i >= len(monitors):

                    i = 0

            currentTiler = self.monitorTilers[monitor][self.currentWorkspace]
            targetTiler = self.monitorTilers[monitors[i]][self.currentWorkspace]
            
            if window in currentTiler.windows:

                currentTiler.windows.remove(window)
                currentTiler.tile_windows()

            if window not in targetTiler.windows:

                targetTiler.windows.append(window)
                targetTiler.tile_windows()

            pwt.utilities.focus(window)

    def handler_alt_shift_D(self):

        window = pwt.utilities.focused_window()
        monitor = pwt.utilities.current_monitor()
        monitors = list(self.monitorTilers.keys())

        if monitor in monitors:

            i = monitors.index(monitor) - 1

            if i < 0:

                    i = len(monitors) - 1

            currentTiler = self.monitorTilers[monitor][self.currentWorkspace]
            targetTiler = self.monitorTilers[monitors[i]][self.currentWorkspace]
            
            if window in currentTiler.windows:

                currentTiler.windows.remove(window)
                currentTiler.tile_windows()

            if window not in targetTiler.windows:

                targetTiler.windows.append(window)
                targetTiler.tile_windows()

            pwt.utilities.focus(window)

    def handler_alt_shift_Q(self):
        "Handles alt+shift+Q, quits the listening"
        
        #stop the polling
        self.stop = True

