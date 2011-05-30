from pwt.hotkeylistener import HotkeyListener
from pwt.windowlistener import WindowListener
from pwt.tiler import Tiler
from pwt.systrayicon import SysTrayIcon

import glob
import time
import pwt.windowutilities

from win32con import MOD_ALT
from win32con import MOD_SHIFT
from win32con import VK_RETURN


class Controller(object):

    def __init__(self):
        "create the hotkey and window listeners on initialization"

        self.ICONFOLDER = "icons/"
        #create <<classname>> based ignorelist
        FLOATS = (#This list may hurt performance if it's huge
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
                , 31: (MOD_ALT + MOD_SHIFT, ord("Q"))
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
                , 31:  self.handler_alt_shift_Q
                }

        self.stop = False
        self.hotkeylistener = HotkeyListener(HOTKEYS, HOTKEYHANDLERS)
        self.windowlistener = WindowListener(FLOATS)

        self.tilers = []
        self.currentTiler = 0
        
        for i in range(9):

            self.tilers.append(Tiler())

        self.systrayicon = SysTrayIcon(self.icon(), "PWT", "PWT")

    def icon(self):
        "Return the appropriate icon"

        return self.ICONFOLDER + str(self.currentTiler + 1) + ".ico"

    ###
    #Commands
    ###

    def start(self):
        "start the listeners with a safety try/finally to unregister keys"

        print("start")
        self.hotkeylistener.register_hotkeys()

        try:

            while not self.stop:

                "Sleep for 0.05 to save resources"
                time.sleep(0.05)

                "Use the listeners"
                self.windowlistener.listen_to_windows(self.tilers[self.currentTiler].tile_windows)
                self.hotkeylistener.listen_to_keys()

        finally:

            print("stop")

            self.hotkeylistener.unregister_hotkeys()


    def switch_tiler(self, i):
        "Switch the current tiler into tiler i"

        #Minize all windows that aren't in the next tiler
        for window in (set(self.tilers[self.currentTiler].windows) - set(self.tilers[i].windows)):

            pwt.windowutilities.minimize(window)

        #Show all windows that weren't in the previous tiler
        for window in (set(self.tilers[i].windows) - set(self.tilers[self.currentTiler].windows)):

            pwt.windowutilities.show(window)

        self.tilers[i].tile_windows()
        self.currentTiler = i
        self.systrayicon.refresh_icon(self.icon())
        self.windowlistener.reload_windows(self.tilers[self.currentTiler].windows)

    def send_window_to_tiler(self, window, i):

        if window in self.tilers[self.currentTiler].windows:

            self.tilers[self.currentTiler].windows.remove(window)
            pwt.windowutilities.minimize(window)

        self.tilers[self.currentTiler].tile_windows()

        if window not in self.tilers[i].windows:

            self.tilers[i].windows.append(window)

    ###
    #Hotkey handlers
    ###

    def handler_alt_H(self):
        "Handles alt+H, decreases the masterwidth"

        self.tilers[self.currentTiler].decrease_masterarea_width()

    def handler_alt_L(self):
        "Handles alt+L, increases the masterwidth"

        self.tilers[self.currentTiler].increase_masterarea_width()

    def handler_alt_J(self):
        "Handles alt+J, sets focus on the next window"

        self.tilers[self.currentTiler].set_focus_down()

    def handler_alt_K(self):
        "Handles alt+K, sets focus on the previous window"

        self.tilers[self.currentTiler].set_focus_up()

    def handler_alt_return(self):
        "Handles alt+RETURN, sets focus on the masterarea"

        self.tilers[self.currentTiler].set_focus_to_masterarea()

    def handler_alt_shift_J(self):
        "Handles alt+shift+J, switches the window to the next position"

        self.tilers[self.currentTiler].move_focusedwindow_down()

    def handler_alt_shift_K(self):
        "Handles alt+shift+K, switches the window to the previous position"

        self.tilers[self.currentTiler].move_focusedwindow_up()

    def handler_alt_shift_return(self):
        "Handles alt+shift+RETURN, switches the window to the masterarea"

        self.tilers[self.currentTiler].move_focusedwindow_to_masterarea()

    def handler_alt_shift_L(self):
        "Handles alt+shift+L, decreases the masterarea size"

        self.tilers[self.currentTiler].decrease_masterarea_size()

    def handler_alt_shift_H(self):
        "Handles alt+shift+H, increases the masterarea size"

        self.tilers[self.currentTiler].increase_masterarea_size()

    def handler_alt_shift_C(self):
        "Handles alt+shift+C, closes the current window"

        window = pwt.windowutilities.get_focused_window()

        pwt.windowutilities.close(window)

    def handler_alt_shift_V(self):
        "Handles alt+shift+V, minimizes the current window"

        window = pwt.windowutilities.get_focused_window()

        pwt.windowutilities.minimize(window)

    def handler_alt_one(self):
        "Handles alt+1, switches tiler"
        
        if self.currentTiler != 0:
            self.switch_tiler(0)

    def handler_alt_two(self):
        "Handles alt+2, switches tiler"
        
        if self.currentTiler != 1:
            self.switch_tiler(1)

    def handler_alt_three(self):
        "Handles alt+3, switches tiler"
        
        if self.currentTiler != 2:
            self.switch_tiler(2)


    def handler_alt_four(self):
        "Handles alt+4, switches tiler"
        
        if self.currentTiler != 3:
            self.switch_tiler(3)


    def handler_alt_five(self):
        "Handles alt+5, switches tiler"
        
        if self.currentTiler != 4:
            self.switch_tiler(4)


    def handler_alt_six(self):
        "Handles alt+6, switches tiler"
        
        if self.currentTiler != 5:
            self.switch_tiler(5)


    def handler_alt_seven(self):
        "Handles alt+7, switches tiler"
        
        if self.currentTiler != 6:
            self.switch_tiler(6)


    def handler_alt_eight(self):
        "Handles alt+8, switches tiler"
        
        if self.currentTiler != 7:
            self.switch_tiler(7)


    def handler_alt_nine(self):
        "Handles alt+9, switches tiler"
        
        if self.currentTiler != 8:
            self.switch_tiler(8)

    def handler_alt_shift_one(self):
        "Handles alt+shift+1, sends window to appropriate tiler"

        window = pwt.windowutilities.get_focused_window() 

        if window:

            self.send_window_to_tiler(window, 0)


    def handler_alt_shift_two(self):
        "Handles alt+shift+2, sends window to appropriate tiler"

        window = pwt.windowutilities.get_focused_window() 

        if window:

            self.send_window_to_tiler(window, 1)

    def handler_alt_shift_three(self):
        "Handles alt+shift+3, sends window to appropriate tiler"

        window = pwt.windowutilities.get_focused_window() 

        if window:

            self.send_window_to_tiler(window, 2)


    def handler_alt_shift_four(self):
        "Handles alt+shift+4, sends window to appropriate tiler"

        window = pwt.windowutilities.get_focused_window() 

        if window:

            self.send_window_to_tiler(window, 3)


    def handler_alt_shift_five(self):
        "Handles alt+shift+5, sends window to appropriate tiler"

        window = pwt.windowutilities.get_focused_window() 

        if window:

            self.send_window_to_tiler(window, 4)


    def handler_alt_shift_six(self):
        "Handles alt+shift+6, sends window to appropriate tiler"

        window = pwt.windowutilities.get_focused_window() 

        if window:

            self.send_window_to_tiler(window, 5)


    def handler_alt_shift_seven(self):
        "Handles alt+shift+7, sends window to appropriate tiler"

        window = pwt.windowutilities.get_focused_window() 

        if window:

            self.send_window_to_tiler(window, 6)


    def handler_alt_shift_eight(self):
        "Handles alt+shift+8, sends window to appropriate tiler"

        window = pwt.windowutilities.get_focused_window() 

        if window:

            self.send_window_to_tiler(window, 7)


    def handler_alt_shift_nine(self):
        "Handles alt+shift+9, sends window to appropriate tiler"

        window = pwt.windowutilities.get_focused_window() 

        if window:

            self.send_window_to_tiler(window, 8)

    def handler_alt_shift_Q(self):
        "Handles alt+shift+Q, quits the listening"

        self.systrayicon.destroy()
        
        #stop the polling
        self.stop = True

